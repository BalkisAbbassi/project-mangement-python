const notificaitonsId = [];
async function checkNotificatiotns() {
  let req = await fetch("http://127.0.0.1:8000/api/messages");
  let msgs = (await req.json()).messages;
  if (notificaitonsId.length === 0) {
    for (const msg of msgs) {
      notificaitonsId.push(msg.id);
    }
  } else {
    for (const msg of msgs) {
      if (!notificaitonsId.includes(msg.id)) {
        notificaitonsId.push(msg.id);
        Push.create(`${msg.from}: ${msg.content}`);
      }
    }
  }
}

setInterval(checkNotificatiotns, 3000);
checkNotificatiotns();
