const socket = new WebSocket('ws://localhost:8000/ws');
socket.addEventListener('open', (event) => {
  console.log('WebSocket connected');
});
socket.addEventListener('message', (event) => {
  const li = document.createElement('li');
  li.innerText = event.data;
  document.querySelector('#events').appendChild(li);
});

document.querySelector('#webhook').addEventListener('click', () => {
  const url = document.querySelector('#input').value;
  socket.send(url);
  document.querySelector('#input').value = '';
});
document.querySelector('#disconnect').addEventListener('click', () => {
socket.send("disconnect");
});
document.querySelector('#send').addEventListener('click', () => {
  const message = document.querySelector('#input').value;
  socket.send(message);
  document.querySelector('#input').value = '';
  });