import json

import gradio as gr


def fizzbuzz(x):
    try:
        x = eval(x)
    except:
        x = 1
    match x:
        case _ if x % 15 == 0:
            return "fizzbuzz"
        case _ if x % 3 == 0:
            return "fizz"
        case _ if x % 5 == 0:
            return "buzz"
        case _:
            return "other"


# waiting for https://github.com/gradio-app/gradio/pull/6680
fizzbuzz_state = {"fizzbuzz": 0, "fizz": 0, "buzz": 0, "other": 0}

default_chat_history = [[None, "Hello!\nI'm FizzBuzz Llama.\nPlease, enter a number"]]

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        value=default_chat_history,
        show_label=False,
        bubble_full_width=False,
        likeable=True,
        avatar_images=(
            None,
            "lama.png",
        ),
    )
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    clear.click(lambda _: default_chat_history, [chatbot], [chatbot])

    def respond(message, chat_history):
        if len(chat_history) == 1:
            for k in fizzbuzz_state.keys():
                fizzbuzz_state[k] = 0
        fizzbuzz_out = fizzbuzz(message)
        fizzbuzz_state[fizzbuzz_out] += 1
        bot_message = json.dumps(
            fizzbuzz_state,
            indent=4,
            separators=(", ", ":\t "),
        )
        bot_message = f"```json\n{bot_message}\n```"
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(auth=("fizz", "buzz"), server_name="0.0.0.0", server_port=5000)
