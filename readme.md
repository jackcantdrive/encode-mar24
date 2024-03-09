# WhatsBot
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

## Overview:
### [1] AI-powered assistant:
(1) User inputs:
  - The recipient's phone number they want to send the message to
  - The message to send
  - The goal: information the AI assistant should always keep in mind when conversing with the recipient
![image](https://github.com/jackpeck/encode-mar24/assets/81492332/30381f86-87c9-4e3d-860b-4d87a57ecdaa)

(2) User are asked to sign into their Whatsapp account, by scanning a QR code
![image](https://github.com/jackpeck/encode-mar24/assets/81492332/68ad7c6f-f4db-4c7b-b117-e2d03a430833)

(3) User press "Submit" on the UI, and a message is sent to the recipient. AI assistant then converse with recipient.
![WhatsApp Image 2024-03-09 at 21 47 11_d7d9e547](https://github.com/jackpeck/encode-mar24/assets/81492332/42d311a5-bfeb-4268-85b9-28301ab0ad97)

### [2] Avatar generator:
(1) User inputs:
  - Description of their ideal avatar
  - (optional) Shape of avatar (circular or square)
  - (optional) Style of avatar
![image](https://github.com/jackpeck/encode-mar24/assets/81492332/b8a8f410-7829-40c1-8e54-a14dee36ca3f)

(2) User press "Generate" to generate the avatar
![image](https://github.com/jackpeck/encode-mar24/assets/81492332/eda32537-ff5d-4cc2-9c7e-88cace170d40)

(3) If user wants to use the generated avatar as their desired profile picture, click "Change whatsapp profile picture" button
(4) Users are asked to sign into their Whatsapp account (same as before), and their avatar is changed 
![image](https://github.com/jackpeck/encode-mar24/assets/81492332/05b20b28-630f-4595-94a2-437b9cf77946)

