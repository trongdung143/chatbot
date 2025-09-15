from typing import Sequence
from langchain_core.tools.base import BaseTool
from time import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools.base import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.agents.base import BaseAgent
from src.agents.state import State
from src.agents.calculator.prompt import prompt
from src.tools.life import get_relative_date, get_time


class CalculatorAgent(BaseAgent):
    def __init__(self, tools: Sequence[BaseTool] | None = None) -> None:
        super().__init__(
            agent_name="calculator",
            tools=[get_relative_date, get_time],
            model=None,
        )

        self._prompt = prompt

        self._chain = self._prompt | self._model

    async def process(self, state: State) -> State:
        start_time = time()

        task_msg = HumanMessage(content=state["task"])
        response = await self._chain.ainvoke({"task": [task_msg]})
        content, human = super().response_filter(response.content)
        logic_result = content.strip() if content else ""
        end_time = time()
        duration = end_time - start_time

        final_task = state["task"] if logic_result == "" else logic_result

        state["agent_logs"].append(
            {
                "agent_name": "calculator",
                "task": state["task"],
                "result": logic_result,
                "step": len(state["agent_logs"]),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
        )

        state["task"] = final_task
        state["prev_agent"] = "calculator"
        state["next_agent"] = "writer"
        state["human"] = human
        return state


# ()
# StateSnapshot(
#     values={
#         "messages": [
#             HumanMessage(
#                 content="ví dụ đạo hàm và tính toán",
#                 additional_kwargs={},
#                 response_metadata={},
#                 id="c150367f-db5a-481b-8231-b09cb10b73a9",
#             ),
#             HumanMessage(
#                 content="ok",
#                 additional_kwargs={},
#                 response_metadata={},
#                 id="eb67012c-2edb-4e19-90f1-96e13f2278e1",
#             ),
#             AIMessage(
#                 content="Chắc chắn rồi, mình sẽ đưa ra một vài ví dụ về đạo hàm và cách tính toán nhé:\n\n**Ví dụ 1: Đạo hàm của hàm số lũy thừa**\n\n*   **Hàm số:** f(x) = x³ + 2x² - 5x + 1\n*   **Quy tắc:** Sử dụng quy tắc đạo hàm của lũy thừa: (xⁿ)' = n*xⁿ⁻¹\n*   **Tính toán:**\n    *   (x³)' = 3x²\n    *   (2x²)' = 4x\n    *   (-5x)' = -5\n    *   (1)' = 0\n*   **Đạo hàm:** f'(x) = 3x² + 4x - 5\n\n**Ví dụ 2: Đạo hàm của hàm số lượng giác**\n\n*   **Hàm số:** g(x) = sin(x) + 2cos(x)\n*   **Quy tắc:** Sử dụng các đạo hàm cơ bản của hàm lượng giác: (sin(x))' = cos(x) và (cos(x))' = -sin(x)\n*   **Tính toán:**\n    *   (sin(x))' = cos(x)\n    *   (2cos(x))' = -2sin(x)\n*   **Đạo hàm:** g'(x) = cos(x) - 2sin(x)\n\n**Ví dụ 3: Đạo hàm của hàm số hợp**\n\n*   **Hàm số:** h(x) = (2x + 1)⁵\n*   **Quy tắc:** Sử dụng quy tắc chuỗi (chain rule): (f(g(x)))' = f'(g(x)) * g'(x)\n*   **Tính toán:**\n    *   Đặt u = 2x + 1, vậy h(x) = u⁵\n    *   h'(x) = (u⁵)' * (2x + 1)' = 5u⁴ * 2 = 10(2x + 1)⁴\n*   **Đạo hàm:** h'(x) = 10(2x + 1)⁴\n\n**Ví dụ 4: Đạo hàm của hàm số phân thức**\n\n*   **Hàm số:** k(x) = (x + 1) / (x - 1)\n*   **Quy tắc:** Sử dụng quy tắc thương (quotient rule): (u/v)' = (u'v - uv') / v²\n*   **Tính toán:**\n    *   u = x + 1, u' = 1\n    *   v = x - 1, v' = 1\n    *   k'(x) = (1*(x - 1) - (x + 1)*1) / (x - 1)² = (-2) / (x - 1)²\n*   **Đạo hàm:** k'(x) = -2 / (x - 1)²\n\nHy vọng những ví dụ này giúp bạn hiểu rõ hơn về cách tính đạo hàm!",
#                 additional_kwargs={},
#                 response_metadata={
#                     "safety_ratings": [],
#                     "finish_reason": "STOP",
#                     "model_name": "gemini-2.0-flash",
#                 },
#                 id="run--b429e562-b0b3-4ff6-b892-7c5cf1230927",
#                 usage_metadata={
#                     "input_tokens": 115,
#                     "output_tokens": 688,
#                     "total_tokens": 803,
#                     "input_token_details": {"cache_read": 0},
#                 },
#             ),
#         ],
#         "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#         "agent_logs": [
#             {
#                 "agent_name": "assigner",
#                 "task": None,
#                 "result": None,
#                 "start_time": None,
#                 "end_time": None,
#                 "duration": None,
#             },
#             {
#                 "agent_name": "assigner",
#                 "task": "ok",
#                 "result": "writer",
#                 "start_time": 1757949856.3580313,
#                 "end_time": 1757949857.0554366,
#                 "duration": 0.6974053382873535,
#             },
#             {
#                 "agent_name": "writer",
#                 "task": "ok",
#                 "result": "Chắc chắn rồi, mình sẽ đưa ra một vài ví dụ về đạo hàm và cách tính toán nhé:\n\n**Ví dụ 1: Đạo hàm của hàm số lũy thừa**\n\n*   **Hàm số:** f(x) = x³ + 2x² - 5x + 1\n*   **Quy tắc:** Sử dụng quy tắc đạo hàm của lũy thừa: (xⁿ)' = n*xⁿ⁻¹\n*   **Tính toán:**\n    *   (x³)' = 3x²\n    *   (2x²)' = 4x\n    *   (-5x)' = -5\n    *   (1)' = 0\n*   **Đạo hàm:** f'(x) = 3x² + 4x - 5\n\n**Ví dụ 2: Đạo hàm của hàm số lượng giác**\n\n*   **Hàm số:** g(x) = sin(x) + 2cos(x)\n*   **Quy tắc:** Sử dụng các đạo hàm cơ bản của hàm lượng giác: (sin(x))' = cos(x) và (cos(x))' = -sin(x)\n*   **Tính toán:**\n    *   (sin(x))' = cos(x)\n    *   (2cos(x))' = -2sin(x)\n*   **Đạo hàm:** g'(x) = cos(x) - 2sin(x)\n\n**Ví dụ 3: Đạo hàm của hàm số hợp**\n\n*   **Hàm số:** h(x) = (2x + 1)⁵\n*   **Quy tắc:** Sử dụng quy tắc chuỗi (chain rule): (f(g(x)))' = f'(g(x)) * g'(x)\n*   **Tính toán:**\n    *   Đặt u = 2x + 1, vậy h(x) = u⁵\n    *   h'(x) = (u⁵)' * (2x + 1)' = 5u⁴ * 2 = 10(2x + 1)⁴\n*   **Đạo hàm:** h'(x) = 10(2x + 1)⁴\n\n**Ví dụ 4: Đạo hàm của hàm số phân thức**\n\n*   **Hàm số:** k(x) = (x + 1) / (x - 1)\n*   **Quy tắc:** Sử dụng quy tắc thương (quotient rule): (u/v)' = (u'v - uv') / v²\n*   **Tính toán:**\n    *   u = x + 1, u' = 1\n    *   v = x - 1, v' = 1\n    *   k'(x) = (1*(x - 1) - (x + 1)*1) / (x - 1)² = (-2) / (x - 1)²\n*   **Đạo hàm:** k'(x) = -2 / (x - 1)²\n\nHy vọng những ví dụ này giúp bạn hiểu rõ hơn về cách tính đạo hàm!",
#                 "step": 2,
#                 "start_time": 1757949857.0721073,
#                 "end_time": 1757949863.220106,
#                 "duration": 6.147998571395874,
#             },
#         ],
#         "next_agent": "writer",
#         "prev_agent": "assigner",
#         "task": "ok",
#         "human": False,
#     },
#     next=(),
#     config={
#         "configurable": {
#             "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#             "checkpoint_ns": "",
#             "checkpoint_id": "1f092480-ece8-6366-8005-49ba8c0ff5d7",
#         }
#     },
#     metadata={
#         "source": "loop",
#         "writes": {
#             "writer": {
#                 "messages": [
#                     HumanMessage(
#                         content="ví dụ đạo hàm và tính toán",
#                         additional_kwargs={},
#                         response_metadata={},
#                         id="c150367f-db5a-481b-8231-b09cb10b73a9",
#                     ),
#                     HumanMessage(
#                         content="ok",
#                         additional_kwargs={},
#                         response_metadata={},
#                         id="eb67012c-2edb-4e19-90f1-96e13f2278e1",
#                     ),
#                     AIMessage(
#                         content="Chắc chắn rồi, mình sẽ đưa ra một vài ví dụ về đạo hàm và cách tính toán nhé:\n\n**Ví dụ 1: Đạo hàm của hàm số lũy thừa**\n\n*   **Hàm số:** f(x) = x³ + 2x² - 5x + 1\n*   **Quy tắc:** Sử dụng quy tắc đạo hàm của lũy thừa: (xⁿ)' = n*xⁿ⁻¹\n*   **Tính toán:**\n    *   (x³)' = 3x²\n    *   (2x²)' = 4x\n    *   (-5x)' = -5\n    *   (1)' = 0\n*   **Đạo hàm:** f'(x) = 3x² + 4x - 5\n\n**Ví dụ 2: Đạo hàm của hàm số lượng giác**\n\n*   **Hàm số:** g(x) = sin(x) + 2cos(x)\n*   **Quy tắc:** Sử dụng các đạo hàm cơ bản của hàm lượng giác: (sin(x))' = cos(x) và (cos(x))' = -sin(x)\n*   **Tính toán:**\n    *   (sin(x))' = cos(x)\n    *   (2cos(x))' = -2sin(x)\n*   **Đạo hàm:** g'(x) = cos(x) - 2sin(x)\n\n**Ví dụ 3: Đạo hàm của hàm số hợp**\n\n*   **Hàm số:** h(x) = (2x + 1)⁵\n*   **Quy tắc:** Sử dụng quy tắc chuỗi (chain rule): (f(g(x)))' = f'(g(x)) * g'(x)\n*   **Tính toán:**\n    *   Đặt u = 2x + 1, vậy h(x) = u⁵\n    *   h'(x) = (u⁵)' * (2x + 1)' = 5u⁴ * 2 = 10(2x + 1)⁴\n*   **Đạo hàm:** h'(x) = 10(2x + 1)⁴\n\n**Ví dụ 4: Đạo hàm của hàm số phân thức**\n\n*   **Hàm số:** k(x) = (x + 1) / (x - 1)\n*   **Quy tắc:** Sử dụng quy tắc thương (quotient rule): (u/v)' = (u'v - uv') / v²\n*   **Tính toán:**\n    *   u = x + 1, u' = 1\n    *   v = x - 1, v' = 1\n    *   k'(x) = (1*(x - 1) - (x + 1)*1) / (x - 1)² = (-2) / (x - 1)²\n*   **Đạo hàm:** k'(x) = -2 / (x - 1)²\n\nHy vọng những ví dụ này giúp bạn hiểu rõ hơn về cách tính đạo hàm!",
#                         additional_kwargs={},
#                         response_metadata={
#                             "safety_ratings": [],
#                             "finish_reason": "STOP",
#                             "model_name": "gemini-2.0-flash",
#                         },
#                         id="run--b429e562-b0b3-4ff6-b892-7c5cf1230927",
#                         usage_metadata={
#                             "input_tokens": 115,
#                             "output_tokens": 688,
#                             "total_tokens": 803,
#                             "input_token_details": {"cache_read": 0},
#                         },
#                     ),
#                 ],
#                 "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#                 "agent_logs": [
#                     {
#                         "agent_name": "assigner",
#                         "task": None,
#                         "result": None,
#                         "start_time": None,
#                         "end_time": None,
#                         "duration": None,
#                     },
#                     {
#                         "agent_name": "assigner",
#                         "task": "ok",
#                         "result": "writer",
#                         "start_time": 1757949856.3580313,
#                         "end_time": 1757949857.0554366,
#                         "duration": 0.6974053382873535,
#                     },
#                     {
#                         "agent_name": "writer",
#                         "task": "ok",
#                         "result": "Chắc chắn rồi, mình sẽ đưa ra một vài ví dụ về đạo hàm và cách tính toán nhé:\n\n**Ví dụ 1: Đạo hàm của hàm số lũy thừa**\n\n*   **Hàm số:** f(x) = x³ + 2x² - 5x + 1\n*   **Quy tắc:** Sử dụng quy tắc đạo hàm của lũy thừa: (xⁿ)' = n*xⁿ⁻¹\n*   **Tính toán:**\n    *   (x³)' = 3x²\n    *   (2x²)' = 4x\n    *   (-5x)' = -5\n    *   (1)' = 0\n*   **Đạo hàm:** f'(x) = 3x² + 4x - 5\n\n**Ví dụ 2: Đạo hàm của hàm số lượng giác**\n\n*   **Hàm số:** g(x) = sin(x) + 2cos(x)\n*   **Quy tắc:** Sử dụng các đạo hàm cơ bản của hàm lượng giác: (sin(x))' = cos(x) và (cos(x))' = -sin(x)\n*   **Tính toán:**\n    *   (sin(x))' = cos(x)\n    *   (2cos(x))' = -2sin(x)\n*   **Đạo hàm:** g'(x) = cos(x) - 2sin(x)\n\n**Ví dụ 3: Đạo hàm của hàm số hợp**\n\n*   **Hàm số:** h(x) = (2x + 1)⁵\n*   **Quy tắc:** Sử dụng quy tắc chuỗi (chain rule): (f(g(x)))' = f'(g(x)) * g'(x)\n*   **Tính toán:**\n    *   Đặt u = 2x + 1, vậy h(x) = u⁵\n    *   h'(x) = (u⁵)' * (2x + 1)' = 5u⁴ * 2 = 10(2x + 1)⁴\n*   **Đạo hàm:** h'(x) = 10(2x + 1)⁴\n\n**Ví dụ 4: Đạo hàm của hàm số phân thức**\n\n*   **Hàm số:** k(x) = (x + 1) / (x - 1)\n*   **Quy tắc:** Sử dụng quy tắc thương (quotient rule): (u/v)' = (u'v - uv') / v²\n*   **Tính toán:**\n    *   u = x + 1, u' = 1\n    *   v = x - 1, v' = 1\n    *   k'(x) = (1*(x - 1) - (x + 1)*1) / (x - 1)² = (-2) / (x - 1)²\n*   **Đạo hàm:** k'(x) = -2 / (x - 1)²\n\nHy vọng những ví dụ này giúp bạn hiểu rõ hơn về cách tính đạo hàm!",
#                         "step": 2,
#                         "start_time": 1757949857.0721073,
#                         "end_time": 1757949863.220106,
#                         "duration": 6.147998571395874,
#                     },
#                 ],
#                 "next_agent": "writer",
#                 "prev_agent": "assigner",
#                 "task": "ok",
#                 "human": False,
#             }
#         },
#         "step": 5,
#         "parents": {},
#         "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#     },
#     created_at="2025-09-15T15:24:23.220106+00:00",
#     parent_config={
#         "configurable": {
#             "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#             "checkpoint_ns": "",
#             "checkpoint_id": "1f092480-b246-6731-8004-5a7c3e5c9f13",
#         }
#     },
#     tasks=(),
#     interrupts=(),
# )


# (
#     Interrupt(
#         value={
#             "AIMessage": 'Chào bạn,Bạn muốn tôi cung cấp ví dụ về đạo hàm và cách tính đạo hàm, đúng không? Để tôi hiểu rõ hơn, bạn có thể cho biết cụ thể hơn về những điều sau không:1.  **Bạn muốn xem ví dụ về những loại hàm số nào?** (ví dụ: hàm đa thức, hàm lượng giác, hàm mũ, hàm logarit, hàm hợp,...)2.  **Bạn muốn tôi trình bày cách tính đạo hàm bằng quy tắc nào?** (ví dụ: quy tắc lũy thừa, quy tắc tích, quy tắc thương, quy tắc chuỗi,...)3.  **Bạn có yêu cầu cụ thể nào về độ khó của ví dụ không?** (ví dụ: ví dụ đơn giản, ví dụ phức tạp, ví dụ có ứng dụng thực tế,...)4.  **Bạn muốn kết quả được trình bày dưới dạng nào?** (ví dụ: công thức, giải thích từng bước,...)Ví dụ, bạn có thể nói: "Tôi muốn xem ví dụ về cách tính đạo hàm của hàm số lượng giác sử dụng quy tắc chuỗi, với độ khó trung bình và có giải thích từng bước."'
#         },
#         resumable=True,
#         ns=[
#             "analyst:41eb3c00-32d9-3d9e-1564-f1ecfaddf53e",
#             "human_node:39f35adf-7539-a51d-dc6d-ffdbf63c0d1b",
#         ],
#     ),
# )
# StateSnapshot(
#     values={
#         "messages": [
#             HumanMessage(
#                 content="ví dụ đạo hàm và tính toán",
#                 additional_kwargs={},
#                 response_metadata={},
#                 id="c150367f-db5a-481b-8231-b09cb10b73a9",
#             )
#         ],
#         "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#         "agent_logs": [
#             {
#                 "agent_name": "assigner",
#                 "task": None,
#                 "result": None,
#                 "start_time": None,
#                 "end_time": None,
#                 "duration": None,
#             },
#             {
#                 "agent_name": "assigner",
#                 "task": "ví dụ đạo hàm và tính toán",
#                 "result": "analyst",
#                 "start_time": 1757949838.590773,
#                 "end_time": 1757949839.7132173,
#                 "duration": 1.1224441528320312,
#             },
#         ],
#         "next_agent": "analyst",
#         "prev_agent": "assigner",
#         "task": "ví dụ đạo hàm và tính toán",
#         "human": False,
#     },
#     next=("analyst",),
#     config={
#         "configurable": {
#             "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#             "checkpoint_ns": "",
#             "checkpoint_id": "1f092480-0cc0-64ad-8001-c0f6b82357f5",
#         }
#     },
#     metadata={
#         "source": "loop",
#         "writes": {
#             "assigner": {
#                 "messages": [
#                     HumanMessage(
#                         content="ví dụ đạo hàm và tính toán",
#                         additional_kwargs={},
#                         response_metadata={},
#                         id="c150367f-db5a-481b-8231-b09cb10b73a9",
#                     )
#                 ],
#                 "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#                 "agent_logs": [
#                     {
#                         "agent_name": "assigner",
#                         "task": None,
#                         "result": None,
#                         "start_time": None,
#                         "end_time": None,
#                         "duration": None,
#                     },
#                     {
#                         "agent_name": "assigner",
#                         "task": "ví dụ đạo hàm và tính toán",
#                         "result": "analyst",
#                         "start_time": 1757949838.590773,
#                         "end_time": 1757949839.7132173,
#                         "duration": 1.1224441528320312,
#                     },
#                 ],
#                 "next_agent": "analyst",
#                 "prev_agent": "assigner",
#                 "task": "ví dụ đạo hàm và tính toán",
#                 "human": False,
#             }
#         },
#         "step": 1,
#         "parents": {},
#         "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#     },
#     created_at="2025-09-15T15:23:59.715652+00:00",
#     parent_config={
#         "configurable": {
#             "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#             "checkpoint_ns": "",
#             "checkpoint_id": "1f092480-0206-6013-8000-d03e43989785",
#         }
#     },
#     tasks=(
#         PregelTask(
#             id="41eb3c00-32d9-3d9e-1564-f1ecfaddf53e",
#             name="analyst",
#             path=("__pregel_pull", "analyst"),
#             error=None,
#             interrupts=(
#                 Interrupt(
#                     value={
#                         "AIMessage": 'Chào bạn,Bạn muốn tôi cung cấp ví dụ về đạo hàm và cách tính đạo hàm, đúng không? Để tôi hiểu rõ hơn, bạn có thể cho biết cụ thể hơn về những điều sau không:1.  **Bạn muốn xem ví dụ về những loại hàm số nào?** (ví dụ: hàm đa thức, hàm lượng giác, hàm mũ, hàm logarit, hàm hợp,...)2.  **Bạn muốn tôi trình bày cách tính đạo hàm bằng quy tắc nào?** (ví dụ: quy tắc lũy thừa, quy tắc tích, quy tắc thương, quy tắc chuỗi,...)3.  **Bạn có yêu cầu cụ thể nào về độ khó của ví dụ không?** (ví dụ: ví dụ đơn giản, ví dụ phức tạp, ví dụ có ứng dụng thực tế,...)4.  **Bạn muốn kết quả được trình bày dưới dạng nào?** (ví dụ: công thức, giải thích từng bước,...)Ví dụ, bạn có thể nói: "Tôi muốn xem ví dụ về cách tính đạo hàm của hàm số lượng giác sử dụng quy tắc chuỗi, với độ khó trung bình và có giải thích từng bước."'
#                     },
#                     resumable=True,
#                     ns=[
#                         "analyst:41eb3c00-32d9-3d9e-1564-f1ecfaddf53e",
#                         "human_node:39f35adf-7539-a51d-dc6d-ffdbf63c0d1b",
#                     ],
#                 ),
#             ),
#             state={
#                 "configurable": {
#                     "thread_id": "097b7540-823e-49d3-982a-f1f0bcbf3aa2",
#                     "checkpoint_ns": "analyst:41eb3c00-32d9-3d9e-1564-f1ecfaddf53e",
#                 }
#             },
#             result=None,
#         ),
#     ),
#     interrupts=(
#         Interrupt(
#             value={
#                 "AIMessage": 'Chào bạn,Bạn muốn tôi cung cấp ví dụ về đạo hàm và cách tính đạo hàm, đúng không? Để tôi hiểu rõ hơn, bạn có thể cho biết cụ thể hơn về những điều sau không:1.  **Bạn muốn xem ví dụ về những loại hàm số nào?** (ví dụ: hàm đa thức, hàm lượng giác, hàm mũ, hàm logarit, hàm hợp,...)2.  **Bạn muốn tôi trình bày cách tính đạo hàm bằng quy tắc nào?** (ví dụ: quy tắc lũy thừa, quy tắc tích, quy tắc thương, quy tắc chuỗi,...)3.  **Bạn có yêu cầu cụ thể nào về độ khó của ví dụ không?** (ví dụ: ví dụ đơn giản, ví dụ phức tạp, ví dụ có ứng dụng thực tế,...)4.  **Bạn muốn kết quả được trình bày dưới dạng nào?** (ví dụ: công thức, giải thích từng bước,...)Ví dụ, bạn có thể nói: "Tôi muốn xem ví dụ về cách tính đạo hàm của hàm số lượng giác sử dụng quy tắc chuỗi, với độ khó trung bình và có giải thích từng bước."'
#             },
#             resumable=True,
#             ns=[
#                 "analyst:41eb3c00-32d9-3d9e-1564-f1ecfaddf53e",
#                 "human_node:39f35adf-7539-a51d-dc6d-ffdbf63c0d1b",
#             ],
#         ),
#     ),
# )
