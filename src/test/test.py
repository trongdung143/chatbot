import asyncio
from src.agents.workflow import graph
from langchain_core.messages import HumanMessage

input_state = {
    "messages": [
        HumanMessage(content="đạo hàm là gì và ví dụ tính toán cụ thể"),
    ],
    "thread_id": "123",
    "agent_logs": [],
    "next_agent": None,
    "prev_agent": None,
    "task": "",
}
config = {"configurable": {"thread_id": "123"}}


async def a():
    async for mode_data in graph.astream(
        input_state,
        config=config,
        stream_mode=["messages", "updates"],
    ):
        mode, payload = mode_data

        if mode == "messages":
            msg, meta = payload
            print(msg.content)


if __name__ == "__main__":
    asyncio.run(a())


{
    "__interrupt__": (
        Interrupt(
            value={"text_to_revise": "original text"},
            resumable=True,
            ns=["human_node:83e3bce4-afd7-f1a6-4104-8a20f85f8b01"],
        ),
    )
}


(
    Interrupt(
        value={
            "AIMessage": "Chào bạn,\n\nBạn muốn tôi cung cấp các ví dụ về đạo hàm, nhưng để tôi hiểu rõ hơn, bạn có thể cho biết cụ thể hơn được không? Ví dụ:\n\n1.  **Bạn muốn loại ví dụ nào?**\n    *   Ví dụ về đạo hàm của các hàm số cơ bản (ví dụ: $x^n$, sin(x), cos(x), e^x, ln(x))?\n    *   Ví dụ về quy tắc tính đạo hàm (ví dụ: quy tắc tích, quy tắc thương, quy tắc chuỗi)?\n    *   Ví dụ về ứng dụng của đạo hàm (ví dụ: tìm cực trị, tìm khoảng đồng biến/nghịch biến, giải bài toán tối ưu)?\n    *   Ví dụ về đạo hàm cấp cao?\n\n2.  **Mức độ phức tạp bạn mong muốn là gì?**\n    *   Ví dụ đơn giản, dễ hiểu?\n    *   Ví dụ phức tạp hơn, đòi hỏi nhiều bước tính toán?\n\n3.  **Bạn có yêu cầu cụ thể nào khác không?**\n    *   Ví dụ có lời giải chi tiết?\n    *   Ví dụ có hình ảnh minh họa?\n\nViệc bạn cung cấp thêm thông tin sẽ giúp tôi đưa ra các ví dụ phù hợp nhất với nhu cầu của bạn."
        },
        resumable=True,
        ns=[
            "analyst:e718becb-6228-5517-b947-59f2400c2e59",
            "human_node:7b9c340f-c76e-c9a1-6641-230ba11935f7",
        ],
    ),
)


(
    ("assigner:f5b90b09-b03f-8207-45bc-56507202f0e6",),
    "messages",
    (
        AIMessageChunk(
            content="writer",
            additional_kwargs={},
            response_metadata={"safety_ratings": []},
            id="run--291b4d19-b0e2-4c31-baf1-d2b39c85d9ad",
            usage_metadata={
                "input_tokens": 293,
                "output_tokens": 0,
                "total_tokens": 293,
                "input_token_details": {"cache_read": 0},
            },
        ),
        {
            "thread_id": "123",
            "langgraph_step": 1,
            "langgraph_node": "assigner",
            "langgraph_triggers": ("branch:to:assigner",),
            "langgraph_path": ("__pregel_pull", "assigner"),
            "langgraph_checkpoint_ns": "assigner:f5b90b09-b03f-8207-45bc-56507202f0e6|assigner:690de630-3a04-9538-36fd-e261587fba12",
            "checkpoint_ns": "assigner:f5b90b09-b03f-8207-45bc-56507202f0e6",
            "ls_provider": "google_genai",
            "ls_model_name": "gemini-2.0-flash",
            "ls_model_type": "chat",
            "ls_temperature": 0.7,
        },
    ),
)


(
    ("memory:dbaf4f5c-d5c2-03f7-b923-460f9ae07a90",),
    "updates",
    {
        "memory": {
            "messages": [
                HumanMessage(
                    content="ý nghĩa vật lý",
                    additional_kwargs={},
                    response_metadata={},
                    id="e310ca87-9615-4990-bb6e-87788b12f9bd",
                ),
                AIMessage(
                    content='"Ý nghĩa vật lý" là một khái niệm rộng, có thể hiểu theo nhiều cách tùy thuộc vào ngữ cảnh cụ thể. Dưới đây là một số cách hiểu phổ biến:\n\n1.  **Giải thích hiện tượng tự nhiên:** Ý nghĩa vật lý của một hiện tượng là sự giải thích nó dựa trên các định luật và nguyên lý vật lý đã được biết đến. Ví dụ:\n\n    *   Ý nghĩa vật lý của việc quả táo rơi từ trên cây xuống là do lực hấp dẫn của Trái Đất tác dụng lên quả táo.\n    *   Ý nghĩa vật lý của cầu vồng là sự tán sắc và phản xạ ánh sáng Mặt Trời qua các giọt nước mưa.\n2.  **Mô tả các đại lượng vật lý:** Ý nghĩa vật lý của một đại lượng vật lý là sự mô tả đại lượng đó đại diện cho điều gì trong thế giới thực. Ví dụ:\n\n    *   Ý nghĩa vật lý của vận tốc là sự thay đổi vị trí của một vật thể theo thời gian.\n    *   Ý nghĩa vật lý của lực là tác động gây ra sự thay đổi trạng thái chuyển động của một vật thể.\n3.  **Ứng dụng của các định luật vật lý:** Ý nghĩa vật lý của một định luật là sự thể hiện định luật đó trong các ứng dụng thực tế. Ví dụ:\n\n    *   Ý nghĩa vật lý của định luật bảo toàn năng lượng là năng lượng không tự sinh ra hoặc mất đi, mà chỉ chuyển đổi từ dạng này sang dạng khác. Điều này có ứng dụng trong việc thiết kế các loại máy móc và công trình tiết kiệm năng lượng.\n4.  **Hiểu bản chất của thế giới:** Ở mức độ sâu sắc hơn, ý nghĩa vật lý có thể liên quan đến việc hiểu bản chất của thế giới xung quanh chúng ta, từ những hạt cơ bản nhất đến cấu trúc của vũ trụ.\n\nTóm lại, "ý nghĩa vật lý" là một khái niệm đa diện, liên quan đến việc giải thích, mô tả và ứng dụng các nguyên lý vật lý để hiểu rõ hơn về thế giới tự nhiên. Để hiểu rõ hơn về ý nghĩa vật lý trong một trường hợp cụ thể, bạn cần cung cấp thêm thông tin về ngữ cảnh mà bạn quan tâm.\n',
                    additional_kwargs={},
                    response_metadata={
                        "safety_ratings": [],
                        "finish_reason": "STOP",
                        "model_name": "gemini-2.0-flash",
                    },
                    id="run--e0a68b81-ce8c-48fd-ac8d-c7c8cc19add8",
                    usage_metadata={
                        "input_tokens": 115,
                        "output_tokens": 472,
                        "total_tokens": 587,
                        "input_token_details": {"cache_read": 0},
                    },
                ),
                HumanMessage(
                    content="đạo hàm là gì",
                    additional_kwargs={},
                    response_metadata={},
                    id="57dca3dc-ad16-4c40-92db-d95c368fb56d",
                ),
                AIMessage(
                    content="Đạo hàm là một khái niệm cơ bản trong giải tích, mô tả tốc độ thay đổi của một hàm số tại một điểm cụ thể. Hiểu một cách đơn giản, đạo hàm cho biết hàm số đang tăng lên, giảm xuống hay không đổi tại điểm đó.\n\n**Định nghĩa:**\n\nCho hàm số y = f(x). Đạo hàm của f(x) tại điểm x, ký hiệu là f'(x) hoặc dy/dx, được định nghĩa là:\n\n```\nf'(x) = lim (h -> 0) [f(x + h) - f(x)] / h\n```\n\nTrong đó:\n\n*   `f(x)` là giá trị của hàm số tại điểm x.\n*   `f(x + h)` là giá trị của hàm số tại điểm x + h (một điểm lân cận x).\n*   `h` là một số rất nhỏ (tiến đến 0).\n\n**Ý nghĩa hình học:**\n\nĐạo hàm f'(x) tại điểm x là hệ số góc của tiếp tuyến với đồ thị hàm số y = f(x) tại điểm có hoành độ x. Nói cách khác, nó cho biết độ dốc của đường cong tại điểm đó.\n\n**Ý nghĩa vật lý:**\n\n*   Nếu y = s(t) là hàm biểu diễn quãng đường đi được của một vật theo thời gian t, thì đạo hàm s'(t) là vận tốc tức thời của vật tại thời điểm t.\n*   Nếu y = v(t) là hàm biểu diễn vận tốc của một vật theo thời gian t, thì đạo hàm v'(t) là gia tốc tức thời của vật tại thời điểm t.\n\n**Cách tính đạo hàm:**\n\nCó nhiều quy tắc và công thức để tính đạo hàm của các hàm số khác nhau. Một số quy tắc cơ bản bao gồm:\n\n*   **Đạo hàm của hằng số:** Nếu f(x) = c (c là hằng số), thì f'(x) = 0.\n*   **Đạo hàm của lũy thừa:** Nếu f(x) = x^n, thì f'(x) = n*x^(n-1).\n*   **Đạo hàm của tổng/hiệu:** Nếu f(x) = u(x) + v(x), thì f'(x) = u'(x) + v'(x).\n*   **Đạo hàm của tích:** Nếu f(x) = u(x) * v(x), thì f'(x) = u'(x) * v(x) + u(x) * v'(x).\n*   **Đạo hàm của thương:** Nếu f(x) = u(x) / v(x), thì f'(x) = [u'(x) * v(x) - u(x) * v'(x)] / [v(x)]^2.\n*   **Quy tắc dây chuyền (đạo hàm của hàm hợp):** Nếu f(x) = g(h(x)), thì f'(x) = g'(h(x)) * h'(x).\n\n**Ví dụ:**\n\n*   Tìm đạo hàm của f(x) = x^2 + 3x - 2.\n    *   f'(x) = 2x + 3\n\n**Ứng dụng của đạo hàm:**\n\nĐạo hàm có rất nhiều ứng dụng trong toán học, vật lý, kỹ thuật, kinh tế và nhiều lĩnh vực khác, bao gồm:\n\n*   Tìm cực trị của hàm số (điểm lớn nhất và nhỏ nhất).\n*   Xác định tính đơn điệu của hàm số (khoảng tăng, giảm).\n*   Giải các bài toán tối ưu hóa.\n*   Mô tả và dự đoán sự thay đổi của các hệ thống động.\n*   Xây dựng các mô hình toán học.\n\nHy vọng điều này giúp bạn hiểu rõ hơn về đạo hàm! Nếu bạn có bất kỳ câu hỏi nào khác, đừng ngần ngại hỏi.\n",
                    additional_kwargs={},
                    response_metadata={
                        "safety_ratings": [],
                        "finish_reason": "STOP",
                        "model_name": "gemini-2.0-flash",
                    },
                    id="run--3e139de4-a959-4e93-929a-fd1429f5d859",
                    usage_metadata={
                        "input_tokens": 592,
                        "output_tokens": 857,
                        "total_tokens": 1449,
                        "input_token_details": {"cache_read": 0},
                    },
                ),
                HumanMessage(
                    content="đạo hàm là gì và phân tích 1 ví dụ thực tế",
                    additional_kwargs={},
                    response_metadata={},
                    id="3f38a0e8-6a51-49e1-b7e9-310d400a8982",
                ),
                AIMessage(
                    content="Như đã giải thích trước đó, đạo hàm là một công cụ toán học dùng để đo tốc độ thay đổi của một hàm số tại một điểm cụ thể. Nó cho biết hàm số đang tăng, giảm hay đứng yên tại điểm đó.\n\n**Ví dụ thực tế: Tốc độ của một chiếc xe**\n\nHãy tưởng tượng bạn đang lái một chiếc xe. Vị trí của xe bạn thay đổi theo thời gian. Ta có thể biểu diễn vị trí của xe như một hàm số `s(t)`, trong đó `s` là vị trí (ví dụ: mét) và `t` là thời gian (ví dụ: giây).\n\n*   **`s(t)`:** Hàm số này cho biết vị trí của xe tại một thời điểm `t` bất kỳ. Ví dụ, `s(5) = 100` có nghĩa là sau 5 giây, xe bạn ở vị trí 100 mét tính từ điểm xuất phát.\n\n*   **Vận tốc trung bình:** Để tính vận tốc trung bình của xe trong một khoảng thời gian, ví dụ từ thời điểm `t1` đến `t2`, ta dùng công thức:\n\n    ```\n    Vận tốc trung bình = (s(t2) - s(t1)) / (t2 - t1)\n    ```\n\n    Ví dụ, nếu `s(2) = 20` và `s(4) = 60`, thì vận tốc trung bình trong khoảng thời gian từ 2 đến 4 giây là `(60 - 20) / (4 - 2) = 20 mét/giây`.\n\n*   **Vận tốc tức thời (đạo hàm):** Vận tốc trung bình chỉ cho biết tốc độ trung bình trong một khoảng thời gian. Nhưng nếu bạn muốn biết vận tốc của xe chính xác tại một thời điểm cụ thể, ví dụ tại thời điểm `t = 3` giây, bạn cần sử dụng đạo hàm.\n\n    Đạo hàm của hàm vị trí `s(t)` theo thời gian `t`, ký hiệu là `s'(t)` hoặc `ds/dt`, chính là vận tốc tức thời của xe tại thời điểm `t`.\n\n    ```\n    v(t) = s'(t) = lim (h -> 0) [s(t + h) - s(t)] / h\n    ```\n\n    Về mặt trực quan, bạn có thể hình dung đạo hàm là vận tốc trung bình được tính trong một khoảng thời gian cực kỳ nhỏ, tiến đến 0.\n\n**Phân tích ví dụ:**\n\nGiả sử hàm vị trí của xe là `s(t) = t^2 + 5t` (với `s` đo bằng mét và `t` đo bằng giây).\n\n1.  **Tìm vận tốc tức thời:** Để tìm vận tốc tức thời `v(t)`, ta cần tính đạo hàm của `s(t)`:\n\n    ```\n    v(t) = s'(t) = d/dt (t^2 + 5t) = 2t + 5\n    ```\n\n2.  **Vận tốc tại thời điểm t = 3 giây:** Để tìm vận tốc của xe tại thời điểm 3 giây, ta thay `t = 3` vào công thức vận tốc:\n\n    ```\n    v(3) = 2(3) + 5 = 11 mét/giây\n    ```\n\n    Vậy, tại thời điểm 3 giây, xe đang di chuyển với vận tốc 11 mét/giây.\n\n**Ý nghĩa của đạo hàm trong ví dụ:**\n\n*   Đạo hàm `v(t) = 2t + 5` cho biết vận tốc của xe *thay đổi* theo thời gian. Vì vận tốc tăng theo thời gian, ta biết rằng xe đang tăng tốc.\n*   Giá trị của đạo hàm tại một thời điểm cụ thể (ví dụ, `v(3) = 11`) cho biết vận tốc chính xác của xe tại thời điểm đó.\n\n**Tóm lại:**\n\nTrong ví dụ này, đạo hàm giúp chúng ta hiểu rõ hơn về chuyển động của xe bằng cách cung cấp thông tin về vận tốc tức thời và cách vận tốc thay đổi theo thời gian. Đây chỉ là một ví dụ đơn giản, nhưng đạo hàm có thể được áp dụng trong nhiều tình huống thực tế khác để phân tích và dự đoán sự thay đổi của các hệ thống.\n",
                    additional_kwargs={},
                    response_metadata={
                        "safety_ratings": [],
                        "finish_reason": "STOP",
                        "model_name": "gemini-2.0-flash",
                    },
                    id="run--b5a3209d-f966-4cd6-b8f3-7435bdf3c4cc",
                    usage_metadata={
                        "input_tokens": 1463,
                        "output_tokens": 948,
                        "total_tokens": 2411,
                        "input_token_details": {"cache_read": 0},
                    },
                ),
                HumanMessage(
                    content="đạo hàm là gì và phân tích 1 ví dụ thực tế",
                    additional_kwargs={},
                    response_metadata={},
                    id="d9a94b6b-c514-42a9-9a0b-32eeb60c29b8",
                ),
                AIMessage(
                    content="Tôi đã giải thích đạo hàm và đưa ra một ví dụ thực tế về tốc độ của xe. Bạn có muốn tôi giải thích thêm về một khía cạnh cụ thể nào đó của đạo hàm, hoặc đưa ra một ví dụ thực tế khác không?\n",
                    additional_kwargs={},
                    response_metadata={
                        "safety_ratings": [],
                        "finish_reason": "STOP",
                        "model_name": "gemini-2.0-flash",
                    },
                    id="run--8e5c9cce-25e6-46a4-aecd-608b9fd0601f",
                    usage_metadata={
                        "input_tokens": 2425,
                        "output_tokens": 52,
                        "total_tokens": 2477,
                        "input_token_details": {"cache_read": 0},
                    },
                ),
                HumanMessage(
                    content="đạo hàm là gì và phân tích 1 ví dụ thực tế",
                    additional_kwargs={},
                    response_metadata={},
                    id="3ba627a5-954d-431b-bbbf-8d8309e6cc1a",
                ),
            ],
            "thread_id": "123",
            "agent_logs": [
                {
                    "agent_name": "assginer",
                    "task": None,
                    "result": None,
                    "start_time": None,
                    "end_time": None,
                    "duration": None,
                },
                {
                    "agent_name": "memory",
                    "task": "skiped",
                    "result": "No summary needed (messages <= 10)",
                    "start_time": 1758124070.7957094,
                    "end_time": 1758124070.7957094,
                    "duration": 0.0,
                },
            ],
            "next_agent": "assigner",
            "prev_agent": "memory",
            "task": "skiped",
            "human": False,
        }
    },
)


(
    ("memory:f50e01bf-6213-ea9e-b720-77f8916f0046",),
    "values",
    {
        "messages": [
            HumanMessage(
                content="đạo hàm là gì và phân tích 1 ví dụ thực tế",
                additional_kwargs={},
                response_metadata={},
                id="d552791b-5774-47ae-9496-979930e6c4be",
            )
        ],
        "thread_id": "123",
        "agent_logs": [
            {
                "agent_name": "assginer",
                "task": None,
                "result": None,
                "start_time": None,
                "end_time": None,
                "duration": None,
            },
            {
                "agent_name": "memory",
                "task": "skiped",
                "result": "No summary needed (messages <= 10)",
                "start_time": 1758124486.0620155,
                "end_time": 1758124486.0620155,
                "duration": 0.0,
            },
        ],
        "next_agent": "assigner",
        "prev_agent": "memory",
        "task": "skiped",
        "human": False,
    },
)


(
    ("analyst:0a5a1ce5-feda-6c62-81a5-dc17df6edbb2",),
    "values",
    {
        "messages": [
            HumanMessage(
                content="đạo hàm là gì và phân tích 1 ví dụ thực tế",
                additional_kwargs={},
                response_metadata={},
                id="d552791b-5774-47ae-9496-979930e6c4be",
            )
        ],
        "thread_id": "123",
        "agent_logs": [
            {
                "agent_name": "assginer",
                "task": None,
                "result": None,
                "start_time": None,
                "end_time": None,
                "duration": None,
            },
            {
                "agent_name": "memory",
                "task": "skiped",
                "result": "No summary needed (messages <= 10)",
                "start_time": 1758124486.0620155,
                "end_time": 1758124486.0620155,
                "duration": 0.0,
            },
            {
                "agent_name": "assigner",
                "task": "đạo hàm là gì và phân tích 1 ví dụ thực tế",
                "result": "analyst\n",
                "start_time": 1758124486.0667136,
                "end_time": 1758124487.0767457,
                "duration": 1.0100321769714355,
            },
            {
                "agent_name": "analyst",
                "task": 'Chào bạn, để làm rõ yêu cầu của bạn, tôi hiểu bạn muốn:\n\n1.  **Định nghĩa:** Giải thích khái niệm "đạo hàm" trong toán học.\n2.  **Ví dụ thực tế:** Phân tích một ví dụ cụ thể, dễ hiểu về ứng dụng của đạo hàm trong đời sống hoặc các lĩnh vực khác.\n\nBạn có muốn tôi tập trung vào một lĩnh vực cụ thể nào cho ví dụ thực tế không (ví dụ: vật lý, kinh tế, kỹ thuật,...)?\n',
                "result": 'Chào bạn, để làm rõ yêu cầu của bạn, tôi hiểu bạn muốn:\n\n1.  **Định nghĩa:** Giải thích khái niệm "đạo hàm" trong toán học.\n2.  **Ví dụ thực tế:** Phân tích một ví dụ cụ thể, dễ hiểu về ứng dụng của đạo hàm trong đời sống hoặc các lĩnh vực khác.\n\nBạn có muốn tôi tập trung vào một lĩnh vực cụ thể nào cho ví dụ thực tế không (ví dụ: vật lý, kinh tế, kỹ thuật,...)?\n',
                "start_time": 1758124487.077646,
                "end_time": 1758124488.9509065,
                "duration": 1.873260498046875,
            },
        ],
        "next_agent": None,
        "prev_agent": "analyst",
        "task": 'Chào bạn, để làm rõ yêu cầu của bạn, tôi hiểu bạn muốn:\n\n1.  **Định nghĩa:** Giải thích khái niệm "đạo hàm" trong toán học.\n2.  **Ví dụ thực tế:** Phân tích một ví dụ cụ thể, dễ hiểu về ứng dụng của đạo hàm trong đời sống hoặc các lĩnh vực khác.\n\nBạn có muốn tôi tập trung vào một lĩnh vực cụ thể nào cho ví dụ thực tế không (ví dụ: vật lý, kinh tế, kỹ thuật,...)?\n',
        "human": True,
    },
)
