from SSconv import SSconv
SSconv.Output("Yo, stock market questions? Ask me!")
while True:
    command = SSconv.Input()
    if command:
        if command in ["exit", "quit", "bye"]:
            SSconv.Output("Peace out, investor!")
            break
        reply = SSconv.GroqReply(command)
        SSconv.Output(reply)
