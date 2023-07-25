const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let playerX = 50;
let playerY = canvas.height - 50;
let playerWidth = 30;
let playerHeight = 30;

function canvasClick(event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    if (
        mouseX >= playerX &&
        mouseX <= playerX + playerWidth &&
        mouseY >= playerY &&
        mouseY <= playerY + playerHeight
    ) {
        playerX = Math.random() * (canvas.width - playerWidth);
        playerY = Math.random() * (canvas.height - playerHeight);
    }
}

canvas.addEventListener('click', canvasClick);

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'red';
    ctx.fillRect(playerX, playerY, playerWidth, playerHeight);

    requestAnimationFrame(gameLoop);
}

gameLoop();
