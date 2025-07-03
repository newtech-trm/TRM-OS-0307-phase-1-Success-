from neomodel import StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, DateTimeProperty, ZeroOrMore, ArrayProperty
from trm_api.graph_models.generates_event import GeneratesEventRel
from trm_api.graph_models.is_part_of_project import IsPartOfProjectRel
from trm_api.graph_models.assigns_task import AssignsTaskRel
from .base import BaseNode

class Task(BaseNode):
    """
    Represents a Task in the TRM-OS ontology.
    A task is a specific action item that is part of a project.
    This model is aligned with the Pydantic TaskBase model and Ontology V3.2.
    """
    # --- Core properties aligned with Ontology V3.2 ---
    name = StringProperty(required=True, index=True, help_text="Tên hoặc tiêu đề ngắn gọn của công việc")
    description = StringProperty(help_text="Mô tả chi tiết về công việc, bao gồm yêu cầu, mục tiêu, tiêu chí hoàn thành")
    
    # Task type & status
    task_type = StringProperty(choices={
        'Feature': 'Feature',
        'Bug': 'Bug', 
        'Chore': 'Chore', 
        'Research': 'Research', 
        'Documentation': 'Documentation', 
        'Meeting': 'Meeting'
    }, help_text="Phân loại công việc, giúp lọc và báo cáo")
    
    status = StringProperty(choices={
        'ToDo': 'ToDo', 
        'InProgress': 'InProgress', 
        'Blocked': 'Blocked', 
        'InReview': 'InReview', 
        'Done': 'Done', 
        'Cancelled': 'Cancelled', 
        'Backlog': 'Backlog'
    }, default='ToDo', help_text="Trạng thái hiện tại của công việc trong quy trình")
    
    # Priority & effort
    priority = IntegerProperty(default=0, help_text="Mức độ ưu tiên của công việc (0-Normal, 1-High, 2-Urgent)")
    effort_estimate = IntegerProperty(help_text="Ước tính công sức hoặc thời gian cần thiết để hoàn thành công việc")
    effort_unit = StringProperty(choices={
        'hours': 'hours', 
        'days': 'days', 
        'story_points': 'story_points'
    }, default='hours', help_text="Đơn vị của effort_estimate")
    
    # Dates
    created_at = DateTimeProperty(default_now=True, help_text="Ngày công việc được tạo")
    updated_at = DateTimeProperty(default_now=True, help_text="Ngày công việc được cập nhật lần cuối")
    start_date = DateTimeProperty(help_text="Ngày bắt đầu dự kiến hoặc thực tế của công việc")
    due_date = DateTimeProperty(help_text="Hạn chót (deadline) cần hoàn thành công việc")
    actual_completion_date = DateTimeProperty(help_text="Ngày công việc thực sự được hoàn thành")
    
    # Assignment & reporting
    assignee_agent_id = StringProperty(help_text="ID của Agent được giao thực hiện công việc này")
    reporter_agent_id = StringProperty(help_text="ID của Agent đã tạo hoặc báo cáo công việc này")
    
    # Categorization
    tags = ArrayProperty(StringProperty(), help_text="Các từ khóa hoặc nhãn để phân loại, tìm kiếm công việc")

    # Dependencies (these are handled through relationships but can also be stored as direct properties)
    dependencies = ArrayProperty(StringProperty(), help_text="Danh sách các taskId khác mà công việc này phụ thuộc vào")
    sub_tasks = ArrayProperty(StringProperty(), help_text="Danh sách các taskId con của công việc này")

    # --- Relationships ---
    # Define the relationship back to the parent project.
    # This complements the 'tasks' relationship in the Project model.
    # Use IsPartOfProjectRel to store relationship properties according to ontology V3.2
    project = RelationshipFrom('trm_api.graph_models.project.Project', 'HAS_TASK', model=IsPartOfProjectRel, cardinality=ZeroOrMore)

    # A task can be assigned to specific users or agents
    # Use AssignsTaskRel to store relationship properties according to ontology V3.2
    assignees_users = RelationshipFrom('trm_api.graph_models.user.User', 'ASSIGNS_TASK', model=AssignsTaskRel, cardinality=ZeroOrMore)
    assignees_agents = RelationshipFrom('trm_api.graph_models.agent.Agent', 'ASSIGNS_TASK', model=AssignsTaskRel, cardinality=ZeroOrMore)

    # A task can block other tasks.
    blocks = RelationshipTo('Task', 'BLOCKS', cardinality=ZeroOrMore)
    blocked_by = RelationshipFrom('Task', 'BLOCKS', cardinality=ZeroOrMore)
    
    # A task can generate events
    # Use GeneratesEventRel to store relationship properties according to ontology V3.2
    generates_events = RelationshipTo('trm_api.graph_models.event.Event', 'GENERATES_EVENT', model=GeneratesEventRel)
    
    # A task can resolve tensions - alignment with Ontology V3.2
    resolves = RelationshipTo('trm_api.graph_models.tension.Tension', 'RESOLVES', cardinality=ZeroOrMore)

    def __str__(self):
        return self.name
