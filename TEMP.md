# Hệ Thống Multi-agent với LangGraph

Hệ thống trợ lý AI đa tác vụ (multi-agent) thông minh với khả năng tương tác tự nhiên và thực hiện nhiều tác vụ phức tạp.

## Tính Năng Chính

- **Tương Tác LLM:** Sử dụng LangChain's MCP để thực thi các tác vụ thông qua Gmail API, Google Drive và xử lý file cục bộ.
- **Bộ Nhớ Dài Hạn:** Lưu trữ lịch sử hội thoại và duy trì ngữ cảnh qua nhiều phiên làm việc trong Supabase (PostgreSQL).
- **Điều Phối Công Cụ Tự Động:** Sử dụng LangGraph để phân tích ý định người dùng và thực thi tác vụ phù hợp.
- **Tự Động Hóa Liền Mạch:** Tích hợp AI hội thoại với các hành động tự động một cách mượt mà.ent with LangGraph

A multi-turn conversational AI assistant with natural, human-like dialogue.

## Features

- **LLM Interaction:** Uses LangChain’s MCP to execute tasks via Gmail API, Google Drive, and local files.
- **Long-Term Memory:** Stores conversation history and multi-session context in Supabase (PostgreSQL).
- **Autonomous Tool Orchestration:** Utilizes LangGraph to perform actions based on user intent.
- **Seamless Task Automation:** Smoothly integrates conversational AI with automated actions.

## Công Nghệ Sử Dụng

### Backend
- Python 3.12+
- FastAPI (Web Framework)
- LangChain & LangGraph (Xử lý ngôn ngữ)
- PostgreSQL/Supabase (Cơ sở dữ liệu)

### API Integration
- Gmail API
- Google Drive API
- OpenAI API
- Anthropic API
- Together API

### ML/AI
- TensorFlow
- Sentence Transformers
- FAISS (Vector Database)

## Cài Đặt và Thiết Lập

### 1. Clone Dự Án
```bash
git clone https://github.com/trongdung143/chatbot.git
cd chatbot
```

### 2. Thiết Lập Môi Trường
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu Hình Môi Trường
Tạo file `.env` với các thông tin sau:
```env
TOGETHER_API_KEY=YOUR_TOGETHER_API_KEY_HERE
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY_HERE
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
SEARCH_ENGINE_ID=YOUR_SEARCH_ENGINE_ID_HERE
CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
CLIENT_ID=YOUR_CLIENT_ID_HERE
REDIRECT_URI=YOUR_REDIRECT_URI_HERE
TOKEN_URL=YOUR_TOKEN_URL_HERE
USERINFO_URL=YOUR_USERINFO_URL_HERE
```

### 5. Khởi Chạy Docker (Tùy chọn)
```bash
docker-compose up -d --build
```

## Cấu Trúc Dự Án

```
├── src/
│   ├── agents/             # Các agent xử lý nhiệm vụ chuyên biệt
│   │   ├── analyst/        # Phân tích dữ liệu và tài liệu
│   │   ├── assigner/       # Phân công nhiệm vụ
│   │   ├── calculator/     # Tính toán và xử lý số liệu
│   │   ├── coder/         # Tạo và phân tích mã nguồn
│   │   ├── memory/        # Quản lý bộ nhớ và ngữ cảnh
│   │   ├── planner/       # Lập kế hoạch và quản lý workflow
│   │   ├── search/        # Tìm kiếm thông tin
│   │   ├── supervisor/    # Giám sát và điều phối
│   │   ├── tool/         # Công cụ hỗ trợ
│   │   ├── vision/       # Xử lý hình ảnh
│   │   └── writer/       # Tạo nội dung và văn bản
│   ├── api/               # Các endpoint API
│   ├── config/            # Cấu hình hệ thống
│   ├── static/            # Tài nguyên tĩnh
│   ├── tools/             # Công cụ tiện ích
│   └── utils/             # Tiện ích chung
├── docker-compose.yml     # Cấu hình Docker Compose
├── Dockerfile            # Định nghĩa Docker container
├── nginx.conf           # Cấu hình Nginx
└── requirements.txt     # Dependency Python
```

## Chức Năng Chi Tiết

### Xử Lý Tài Liệu và Chat
- Phân tích tài liệu với RAG (Retrieval-Augmented Generation)
- Giao diện chat thời gian thực
- Xử lý đa luồng hội thoại
- Tích hợp bộ nhớ dài hạn

### Quản Lý File và Dữ Liệu
- Tải lên/tải xuống file
- Tích hợp với PostgreSQL
- Lưu trữ và truy xuất vector
- Xử lý định dạng đa dạng

### Triển Khai và Bảo Mật
- Container hóa với Docker
- Reverse Proxy qua Nginx
- Xác thực và phân quyền
- Giám sát hệ thống

## Yêu Cầu Hệ Thống

### Phần Mềm
- Python 3.12 trở lên
- PostgreSQL Database
- Docker (tùy chọn)
- Nginx (cho môi trường production)

### Tài Nguyên
- RAM: Tối thiểu 4GB
- CPU: 2 cores trở lên
- Ổ cứng: 10GB trống
- Kết nối Internet ổn định

## Khởi Tạo Cơ Sở Dữ Liệu

### Cấu Hình PostgreSQL
1. Tạo database mới:
```sql
CREATE DATABASE chatbot;
```

2. Khởi tạo schema:
```bash
python -m src.config.setup
```

### Thiết Lập Vector Store
1. Cài đặt FAISS:
```bash
pip install faiss-cpu  # hoặc faiss-gpu cho GPU
```

2. Khởi tạo vector store:
```python
from src.utils.vectorst import init_vector_store
init_vector_store()
```

### Khởi Tạo Cache
1. Cấu hình Redis (tùy chọn):
```bash
redis-cli config set maxmemory 2gb
redis-cli config set maxmemory-policy allkeys-lru
```

2. Khởi động cache service:
```bash
python -m src.config.cache
```

## Chạy Ứng Dụng

### Môi Trường Phát Triển
```bash
# Khởi động server development
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload

# Chạy với hot reload và debug mode
python -m uvicorn src.main:app --reload --log-level debug
```

### Sử Dụng Docker
```bash
# Build và chạy tất cả container
docker-compose up -d --build

# Xem logs
docker-compose logs -f

# Dừng các container
docker-compose down
```

## API Endpoints

### 1. Chat Interface (`/api/chat`)
- POST `/api/chat/message` - Gửi tin nhắn mới
- GET `/api/chat/history` - Lấy lịch sử chat
- DELETE `/api/chat/clear` - Xóa lịch sử

### 2. Authentication (`/api/login`)
- POST `/api/login` - Đăng nhập
- POST `/api/logout` - Đăng xuất
- GET `/api/user/profile` - Thông tin người dùng

### 3. File Management (`/api/download`)
- POST `/api/upload` - Tải file lên
- GET `/api/download/{file_id}` - Tải file xuống
- GET `/api/files/list` - Danh sách file

### 4. System Management (`/api/home`)
- GET `/api/status` - Trạng thái hệ thống
- GET `/api/stats` - Thống kê sử dụng
- POST `/api/config/update` - Cập nhật cấu hình

## Cấu Hình Hệ Thống

### Database (`src/config/database.py`)
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@localhost/chatbot"
POOL_SIZE = 20
MAX_OVERFLOW = 10
POOL_TIMEOUT = 30
```

### Cài Đặt Chung (`src/config/setup.py`)
```python
DEBUG = True
LOG_LEVEL = "INFO"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
```

## Phát Triển

## Kiến Trúc và Phát Triển Agent

### 1. Cấu Trúc Agent

#### 1.1 Base Agent
Mọi agent đều kế thừa từ class `BaseAgent`:
```python
from typing import Any, Dict, Optional
from src.agents.base import BaseAgent
from src.utils.handler import MessageHandler

class BaseAgent:
    def __init__(self):
        self.name: str = "base_agent"
        self.description: str = "Base agent for inheritance"
        self.handler: MessageHandler = MessageHandler()
        self.memory: Dict[str, Any] = {}
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý input và trả về kết quả
        Args:
            input_data: Dữ liệu đầu vào cần xử lý
        Returns:
            Dict chứa kết quả xử lý
        """
        raise NotImplementedError
        
    async def _pre_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Tiền xử lý dữ liệu trước khi process chính"""
        return data
        
    async def _post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Hậu xử lý kết quả sau process chính"""
        return result
```

#### 1.2 Specialized Agent
Ví dụ về một agent chuyên biệt:

```python
from src.agents.base import BaseAgent
from src.utils.converter import DataConverter
from src.utils.vectorst import VectorStore

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "analyst"
        self.description = "Agent phân tích dữ liệu và tài liệu"
        self.vector_store = VectorStore()
        self.converter = DataConverter()
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Tiền xử lý
        cleaned_data = await self._pre_process(input_data)
        
        # 2. Phân tích dữ liệu
        analysis_result = await self._analyze_data(cleaned_data)
        
        # 3. Vector embedding
        if "text" in cleaned_data:
            vectors = await self.vector_store.embed_text(cleaned_data["text"])
            analysis_result["vectors"] = vectors
            
        # 4. Tạo recommendations
        recommendations = await self._generate_recommendations(analysis_result)
        
        # 5. Hậu xử lý và trả về
        return await self._post_process({
            "analysis": analysis_result,
            "recommendations": recommendations,
            "metadata": {
                "agent": self.name,
                "timestamp": self.handler.get_timestamp()
            }
        })
        
    async def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích dữ liệu chi tiết"""
        # Logic phân tích...
        return analysis_result
        
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Tạo recommendations dựa trên kết quả phân tích"""
        # Logic tạo recommendations...
        return recommendations
```

### 2. Tích Hợp Agent Vào Workflow

#### 2.1 Đăng Ký Agent
Trong `workflow.py`:
```python
from src.agents.analyst import AnalystAgent
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent

class AgentWorkflow:
    def __init__(self):
        self.agents = {}
        self.pipeline = []
        
    def register_agent(self, agent: BaseAgent):
        """Đăng ký agent mới vào workflow"""
        self.agents[agent.name] = agent
        
    def create_pipeline(self, order: List[str]):
        """Tạo pipeline xử lý với thứ tự các agent"""
        self.pipeline = [self.agents[name] for name in order]
        
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi pipeline xử lý"""
        result = input_data
        for agent in self.pipeline:
            result = await agent.process(result)
        return result

# Khởi tạo workflow
workflow = AgentWorkflow()
workflow.register_agent(AnalystAgent())
workflow.register_agent(PlannerAgent())
workflow.register_agent(ExecutorAgent())

# Thiết lập pipeline
workflow.create_pipeline(["analyst", "planner", "executor"])
```

### 3. Xử Lý Prompt và Memory

#### 3.1 Prompt Template
Trong `src/agents/analyst/prompt.py`:
```python
from string import Template

ANALYSIS_PROMPT = Template("""
Analyze the following data:
$data

Focus on:
1. Key insights
2. Patterns and trends
3. Potential issues
4. Recommendations

Context: $context
""")

class PromptManager:
    def __init__(self):
        self.templates = {
            "analysis": ANALYSIS_PROMPT
        }
    
    def get_prompt(self, template_name: str, **kwargs) -> str:
        """Lấy prompt với các tham số động"""
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template {template_name} not found")
        return template.substitute(**kwargs)
```

#### 3.2 Memory Management
```python
class AgentMemory:
    def __init__(self):
        self.short_term: Dict[str, Any] = {}
        self.long_term: Dict[str, Any] = {}
        self.context_window: List[Dict] = []
        
    async def add_to_memory(self, data: Dict[str, Any], memory_type: str = "short"):
        """Thêm dữ liệu vào memory"""
        if memory_type == "short":
            self.short_term.update(data)
        else:
            self.long_term.update(data)
            
    async def get_from_memory(self, key: str, memory_type: str = "short") -> Any:
        """Lấy dữ liệu từ memory"""
        memory = self.short_term if memory_type == "short" else self.long_term
        return memory.get(key)
        
    async def update_context_window(self, new_context: Dict):
        """Cập nhật context window"""
        self.context_window.append(new_context)
        if len(self.context_window) > 10:  # Giữ 10 context gần nhất
            self.context_window.pop(0)
```
```

### 4. Triển Khai Các Loại Agent

#### 4.1 Search Agent
Agent chuyên về tìm kiếm và truy xuất thông tin:
```python
class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "search"
        self.vector_db = VectorStore()
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query")
        search_type = input_data.get("type", "semantic")
        
        if search_type == "semantic":
            results = await self.semantic_search(query)
        elif search_type == "keyword":
            results = await self.keyword_search(query)
        else:
            results = await self.hybrid_search(query)
            
        return {
            "results": results,
            "metadata": {"search_type": search_type}
        }
```

#### 4.2 Memory Agent
Agent quản lý bộ nhớ và context:
```python
class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "memory"
        self.memory_store = AgentMemory()
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Xử lý input và cập nhật memory
        action = input_data.get("action")
        
        if action == "store":
            await self.memory_store.add_to_memory(
                input_data["data"],
                input_data.get("memory_type", "short")
            )
        elif action == "retrieve":
            result = await self.memory_store.get_from_memory(
                input_data["key"],
                input_data.get("memory_type", "short")
            )
            return {"retrieved_data": result}
```

#### 4.3 Supervisor Agent
Agent giám sát và điều phối:
```python
class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "supervisor"
        self.active_agents = {}
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Phân tích task và chọn agent phù hợp
        task_type = await self._analyze_task(input_data)
        selected_agents = await self._select_agents(task_type)
        
        # Tạo và thực thi workflow
        workflow = await self._create_workflow(selected_agents)
        result = await workflow.execute(input_data)
        
        # Giám sát và điều chỉnh nếu cần
        if await self._need_adjustment(result):
            result = await self._adjust_and_retry(workflow, input_data)
            
        return result
```

### 5. Testing Agents

#### 5.1 Unit Testing
```python
import pytest
from src.agents.analyst import AnalystAgent

@pytest.fixture
def analyst_agent():
    return AnalystAgent()

async def test_analyst_process():
    agent = analyst_agent()
    input_data = {
        "text": "Sample text for analysis",
        "context": {"domain": "technology"}
    }
    
    result = await agent.process(input_data)
    
    assert "analysis" in result
    assert "recommendations" in result
    assert result["metadata"]["agent"] == "analyst"
```

#### 5.2 Integration Testing
```python
async def test_workflow_integration():
    workflow = AgentWorkflow()
    workflow.register_agent(AnalystAgent())
    workflow.register_agent(PlannerAgent())
    
    input_data = {
        "task": "analyze_document",
        "content": "Sample document content"
    }
    
    result = await workflow.execute(input_data)
    
    assert result["status"] == "success"
    assert "analysis_result" in result
    assert "plan" in result
```

### 3. Tùy Chỉnh Workflow

Trong `src/agents/workflow.py`:
```python
class CustomWorkflow(BaseWorkflow):
    def __init__(self):
        super().__init__()
        self.add_step("analyze", AnalystAgent())
        self.add_step("process", ProcessorAgent())
        self.add_step("respond", ResponderAgent())
```

## Kiểm Thử

### Unit Tests
```bash
# Chạy tất cả test
python -m pytest tests/

# Chạy test cụ thể
pytest tests/test_agents.py

# Với coverage report
pytest --cov=src --cov-report=html tests/
```

### Integration Tests
```bash
# Tests API endpoints
pytest tests/api/
```

### Load Tests
```bash
# Sử dụng locust
locust -f tests/locustfile.py
```

## Triển Khai

### 1. Sử Dụng Docker

```bash
# Build image
docker build -t chatbot:latest .

# Chạy container
docker run -d -p 8080:8080 chatbot:latest

# Scale với docker-compose
docker-compose up -d --scale web=3
```

### 2. Triển Khai Thủ Công

Cấu hình Nginx (`nginx.conf`):
```nginx
server {
    listen 80;
    server_name chatbot.example.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Chạy với gunicorn:
```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080
```

## Script Hệ Thống

Thư mục `src/config/system/` chứa các script:

### Server Management
- `restart_server.ps1`: Khởi động lại server
- `backup_db.ps1`: Sao lưu database
- `update_system.ps1`: Cập nhật hệ thống

### Development Tools
- `ngrok.ps1`: Thiết lập tunnel
- `generate_docs.ps1`: Tạo documentation
- `run_tests.ps1`: Chạy test suite

## Đóng Góp

### Quy Trình Đóng Góp
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/TinhNangMoi`)
3. Commit thay đổi (`git commit -m 'Thêm tính năng mới'`)
4. Push lên branch (`git push origin feature/TinhNangMoi`)
5. Tạo Pull Request

### Tiêu Chuẩn Code
- Tuân thủ PEP 8 cho Python code
- Viết docstring cho functions và classes
- Có unit test cho code mới
- Cập nhật documentation khi cần

### Báo Lỗi
- Sử dụng GitHub Issues để báo lỗi
- Mô tả chi tiết vấn đề gặp phải
- Cung cấp các bước để tái hiện lỗi
- Đính kèm logs nếu có

## Giấy Phép
Dự án được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## Tác Giả
- **Trọng Dũng** - *Tác giả chính* - [trongdung143](https://github.com/trongdung143)

## Liên Hệ
- Email: trongdung143@gmail.com
- GitHub: [@trongdung143](https://github.com/trongdung143)
- Website: [example.com](https://example.com)

## Ghi Nhận
Cảm ơn tất cả những người đã đóng góp cho dự án này. Đặc biệt cảm ơn:
- Cộng đồng LangChain
- Cộng đồng FastAPI
- Các contributor đã đóng góp code và ý tưởng
