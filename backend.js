const apiKey = "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";

const OpenAI = require('openai');

const express = require('express');
const MessageMedia = require('whatsapp-web.js').MessageMedia;
const bodyParser = require('body-parser');
const app = express();
const port = 3000;
const cors = require('cors');

const openai = new OpenAI({apiKey: apiKey});

async function generateText(context) {
    const completion = await openai.chat.completions.create({
        messages: context,
        model: "gpt-3.5-turbo",
    });
    return completion.choices[0].message.content;
}

const { Client, Location, Poll, List, Buttons, LocalAuth } = require('whatsapp-web.js');

const client = new Client({
    authStrategy: new LocalAuth(),
    // proxyAuthentication: { username: 'username', password: 'password' },
    puppeteer: { 
        // args: ['--proxy-server=proxy-server-that-requires-authentication.example.com'],
        headless: false
    }
});

function authenticateUser() {
    return new Promise((resolve, reject) => {
        client.initialize();

        client.on('loading_screen', (percent, message) => {
            console.log('LOADING SCREEN', percent, message);
        });

        client.on('qr', (qr) => {
            console.log('QR RECEIVED', qr);
        });

        client.on('authenticated', () => {
            console.log('AUTHENTICATED');
            resolve(true);
        });

        client.on('auth_failure', msg => {
            console.error('AUTHENTICATION FAILURE', msg);
            resolve(false);
        });
    });
}

let isReady = false;

async function clientReady() {
    return new Promise((resolve, reject) => {

        if (isReady) {
            resolve(true);
            return;
        }

        client.on('ready', () => {
            isReady = true;
            console.log('READY');
            resolve(true);
        });
    });
}

client.promises ??= {};
client.promises.sendMessage = (number, message) => {
    return new Promise((resolve, reject) => {
        client.sendMessage(number, message);
        resolve();
    });
}

const clientOnMessageHandlers = [];
const addClientOnMessageHandler = (handler) => {
    clientOnMessageHandlers.push(handler);

    return handler;
}

const removeClientOnMessageHandler = (handler) => {
    const index = clientOnMessageHandlers.indexOf(handler);
    if (index > -1) {
        clientOnMessageHandlers.splice(index, 1);
    }
}

client.on('message', async msg => {
    for (const handler of clientOnMessageHandlers) {
        await handler(msg);
    }
});

async function sends_message(number, message, additional) {
    await clientReady();

    const startTimestamp = Date.now();

    const context = [];

    const sendMessage = async (message) => {
        await client.promises.sendMessage(number, message);
        context.push({"role": "assistant", "content": message});
    }

    await sendMessage(message);

    const handler = addClientOnMessageHandler(async msg => {
        if (msg.from === number && msg.timestamp * 1000 > startTimestamp) {
            console.log('MESSAGE RECEIVED', msg);

            context.push({"role": "user", "content": msg.body});
            context.push({role: "system", content: "you are a physical human replying to another physical human via text. Keep the reply short."});
            const prompt = "Generate a response message for: "+msg.body+"\n Keep in mind: "+additional;
            context.push({"role": "system", "content": prompt});
            const response = await generateText(context);
            await sendMessage(response);
        }
    });
}

async function change_avatar(img_data) {
    await clientReady();
    await client.setProfilePicture(MessageMedia.fromFilePath("avatar.png"));
}

const setupWhatsappWeb = async () => {
    const isAuthenticated = await authenticateUser();
    console.log('isAuthenticated', isAuthenticated);
    if (!isAuthenticated) {
        console.error("Authentication failed. Message not sent.");
    }

    await clientReady();
}

app.use(bodyParser.json());
app.use(cors());

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});

app.post('/sends-message', async (req, res) => {
    const {number: rawNumber, message, additional} = req.body;
    const number = rawNumber.replace('+', ''); // remove + from number

    const prompt = "Generate a a text message for: "+message+"\n Keep in mind: "+additional;
    const context = [{role: "system", content: "you are a physical human texting another physical human. Keep it short."}, {role: "system", content: prompt}]
    const to_send = await generateText(context);
    sends_message(number + '@c.us', to_send, additional);
    res.send({msg:to_send});
});

app.post('/change-avatar', async (req, res) => {
    const {img_data} = req.body;
    change_avatar(img_data);
    res.send({msg:"Avatar changed"});
});

setupWhatsappWeb();
