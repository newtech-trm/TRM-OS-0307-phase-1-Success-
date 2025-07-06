#!/usr/bin/env python3
"""Fix all test methods to include cleanup"""

import re

def fix_test_file():
    with open('tests/unit/test_adaptive_learning_system.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find test methods that use learning_system
    test_pattern = r'(    @pytest\.mark\.asyncio\s+async def test_\w+\(self, learning_system[^)]*\):\s*"""[^"]*"""\s*)(.*?)(\n    @pytest\.mark\.asyncio|\n    def test_|\nclass|\Z)'
    
    def add_cleanup(match):
        method_start = match.group(1)
        method_body = match.group(2)
        next_part = match.group(3)
        
        # Skip if already has cleanup
        if 'await self.cleanup_system(learning_system)' in method_body:
            return match.group(0)
        
        # Add try/finally with cleanup
        lines = method_body.split('\n')
        
        # Find the first non-empty line to determine indentation
        first_line_indent = ''
        for line in lines:
            if line.strip():
                first_line_indent = line[:len(line) - len(line.lstrip())]
                break
        
        # Wrap existing content in try/finally
        new_body = f'{first_line_indent}try:\n'
        for line in lines:
            if line.strip():
                new_body += f'    {line}\n'
            else:
                new_body += line + '\n'
        
        new_body += f'{first_line_indent}finally:\n'
        new_body += f'{first_line_indent}    # Cleanup background tasks\n'
        new_body += f'{first_line_indent}    await self.cleanup_system(learning_system)\n'
        
        return method_start + new_body + next_part
    
    # Apply the fix
    fixed_content = re.sub(test_pattern, add_cleanup, content, flags=re.DOTALL)
    
    # Write back
    with open('tests/unit/test_adaptive_learning_system.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed all test methods with cleanup")

if __name__ == "__main__":
    fix_test_file() 