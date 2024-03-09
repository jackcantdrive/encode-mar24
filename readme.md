# WhatzBot
## Design Brief
Our project offers 2 innovative tools for whatsapp:
### [1] AI-powered assistant:
Tired of repetitive tasks like reminding your brother to feed the dog or scheduling the same event with a lot of people? Our AI assistant handles those conversations for you. It can initiate chats, send messages, and even respond to replies, saving you valuable time. This feature also comes in handy for awkward requests, like reminding someone to pay you back.
### [2] Custom avatar generator:
Ever wish you could have the perfect WhatsApp avatar? Our generator use generative AI to let you design one to your specifications. Simply describe your ideal avatar, and our tool will create it. Once you find one you love, you can seamlessly set it as your profile picture with a single click.

## Tech Stack:
- Client: written in Python using Gradio, designed to be a web based Whatsapp tool.
- Backend: written in JavaScript using Node.js
  - Server: express
  - Assistant using GPT-3.5 API
  - Avatar generator using Stability AI's text-to-image model's API
  - Sending, receiving messages and changing avatar in Whatsapp using [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js)

## Tools:
- GitHub for code hosting, CI, code review, project management
- VS Code IDE

