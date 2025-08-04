const mineflayer = require('mineflayer');
const readline = require('readline');
const { pathfinder, Movements, goals } = require('mineflayer-pathfinder');
const fs = require('fs');
const path = require('path');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

let bot;
let afkInterval;
let followPlayer;
let movementState = {};

function createBot(name, host, port) {
    bot = mineflayer.createBot({
        host: host,
        port: port,
        username: name,
        version: '1.18' // cambia la version si querers
    });

    bot.loadPlugin(pathfinder);

    bot.on('login', () => {
        console.log(`Bot ${bot.username} conectado.`);
    });

    bot.on('chat', (username, message) => {
        if (username === bot.username) return;
        console.log(`[${bot.username}] ${username}: ${message}`);
    });

    bot.on('message', (message) => {
        console.log(`Servidor: ${message.toString()}`);
    });

    bot.on('error', (err) => console.log(`Error en ${bot.username}: ${err.message}`));
    bot.on('end', () => console.log(`Bot ${bot.username} desconectado.`));

    bot.on('playerJoined', (player) => {
        if (bot.username !== player.username) {
        }
    });

    bot.on('playerLeft', (player) => {
    });
}

function saveOnlineUsers() {
    if (!bot.players) return;

    const onlineUsers = Object.keys(bot.players).map(playerName => playerName);

    const filePath = path.join(__dirname, 'nick_safe', `${bot.host}.txt`);
    fs.mkdirSync(path.dirname(filePath), { recursive: true });

    const content = onlineUsers.join('\n');
    fs.writeFileSync(filePath, content);
    console.log('Usuarios guardados');
}

function interactWithNpc() {
    const entities = bot.entities;

    let closestNpc = null;
    let minDistance = 5;

    for (const id in entities) {
        const entity = entities[id];
        if (entity.type === 'mob' && entity.mobType === 'Villager') {
            const distance = bot.entity.position.distanceTo(entity.position);
            if (distance < minDistance) {
                closestNpc = entity;
                minDistance = distance;
            }
        }
    }

    if (closestNpc) {
        console.log(`Interaccionando con el NPC ${closestNpc.displayName}`);
        bot.activateEntity(closestNpc);
    } else {
        console.log('No hay NPCs cercanos para interactuar.');
    }
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.error('Uso: node bot.js <nombre_bot> <ip> [puerto]');
    process.exit(1);
}

const nombreBot = args[0];
const ip = args[1];
const puerto = args[2] ? parseInt(args[2]) : 25565;

createBot(nombreBot, ip, puerto);

console.log('Escribe .help para ver los comandos disponibles.');
rl.on('line', (input) => {
    if (input === '.remove') {
        if (bot) {
            console.log('Desconectando el bot...');
            bot.end();
        }
    } else if (input === '.restart') {
        if (bot) {
            console.log('Reiniciando el bot...');
            bot.end();
            setTimeout(() => createBot(nombreBot, ip, puerto), 3000);
        }
    } else if (input === '.help') {
        console.log('Comandos disponibles:');
        console.log('.remove    - Desconectar el bot');
        console.log('.restart   - Reiniciar el bot');
        console.log('.clear     - Limpiar la consola');
        console.log('.afk       - Activar modo AFK');
        console.log('.afkstop   - Detener modo AFK');
        console.log('.goplayer <nick> - Seguir a un jugador');
        console.log('.derecho   - Hacer clic derecho');
        console.log('.izquierdo - Hacer clic izquierdo');
        console.log('.adelante  - Avanzar');
        console.log('.atras     - Retroceder');
        console.log('.derecha   - Moverse a la derecha');
        console.log('.izquierda - Moverse a la izquierda');
        console.log('.stop      - Detener movimiento y seguimiento');
        console.log('.safetab   - Guardar usuarios online en un archivo');
    } else if (input === '.safetab') {
        saveOnlineUsers();
    } else if (input === '.derecho') {
        bot.activateItem();
    } else if (input === '.izquierdo') {
        bot.swingArm('right');
    } else if (input === '.clear') {
        console.clear();
    } else if (input === '.afk') {
        if (!afkInterval) {
            console.log('Modo AFK activado.');
            afkInterval = setInterval(() => {
                if (bot) {
                    bot.setControlState('jump', true);
                    bot.swingArm('right');
                    bot.look(Math.random() * Math.PI * 2, Math.random() * Math.PI - Math.PI / 2, true);
                }
            }, 1000);
        }
    } else if (input === '.afkstop') {
        console.log('Modo AFK desactivado.');
        clearInterval(afkInterval);
        afkInterval = null;
        if (bot) bot.setControlState('jump', false);
    } else if (input.startsWith('.goplayer')) {
        const args = input.split(' ');
        const targetName = args[1];

        if (!targetName) {
            console.log('Debes especificar un nombre de jugador.');
            return;
        }

        const player = bot.players[targetName]?.entity;

        if (!player) {
            console.log(`No se encontró al jugador ${targetName}.`);
            return;
        }

        console.log(`Siguiendo a ${targetName}.`);
        followPlayer = setInterval(() => {
            if (player) {
                bot.pathfinder.setGoal(new goals.GoalFollow(player, 1), true);
            } else {
                console.log(`${targetName} ya no está cerca.`);
                clearInterval(followPlayer);
                followPlayer = null;
            }
        }, 1000);
    } else if (['.adelante', '.atras', '.derecha', '.izquierda'].includes(input)) {
        const directionMap = {
            '.adelante': 'forward',
            '.atras': 'back',
            '.derecha': 'right',
            '.izquierda': 'left'
        };

        let direction = directionMap[input];

        if (!movementState[direction]) {
            console.log(`Moviéndose hacia ${input.slice(1)}.`);
            bot.setControlState(direction, true);
            movementState[direction] = true;
        } else {
            console.log(`Deteniendo movimiento ${input.slice(1)}.`);
            bot.setControlState(direction, false);
            movementState[direction] = false;
        }
    } else if (input === '.stop') {
        console.log('Deteniendo todos los movimientos y el seguimiento.');
        Object.keys(movementState).forEach(dir => bot.setControlState(dir, false));
        movementState = {};
        
        if (followPlayer) {
            clearInterval(followPlayer);
            followPlayer = null;
            bot.pathfinder.setGoal(null);
        }
    } else {
        if (bot) bot.chat(input);
    }
});
