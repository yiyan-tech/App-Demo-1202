document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('textInput');
    const voiceBtn = document.getElementById('voiceBtn');
    const generateBtn = document.getElementById('generateBtn');
    const clearBtn = document.getElementById('clearBtn');
    const statusDiv = document.getElementById('status');
    const canvasArea = document.getElementById('canvas-area');
    const placeholderText = document.querySelector('.placeholder-text');

    let zIndexCounter = 1;

    // --- 语音识别功能 ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN'; // 设置为中文，也可以根据需要改为 'en-US'
        recognition.continuous = false;
        recognition.interimResults = false;

        voiceBtn.addEventListener('click', () => {
            if (voiceBtn.classList.contains('recording')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });

        recognition.onstart = () => {
            voiceBtn.classList.add('recording');
            voiceBtn.textContent = '🛑 停止录音';
            statusDiv.textContent = '正在聆听...';
        };

        recognition.onend = () => {
            voiceBtn.classList.remove('recording');
            voiceBtn.textContent = '🎤 语音输入';
            statusDiv.textContent = '就绪';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            textInput.value = transcript;
            statusDiv.textContent = `识别结果: "${transcript}"`;
            // 可选：语音输入结束后直接生成
            // generateGraphic(transcript);
        };

        recognition.onerror = (event) => {
            console.error(event.error);
            statusDiv.textContent = '语音识别错误: ' + event.error;
            voiceBtn.classList.remove('recording');
            voiceBtn.textContent = '🎤 语音输入';
        };
    } else {
        voiceBtn.disabled = true;
        voiceBtn.textContent = '不支持语音';
        statusDiv.textContent = '您的浏览器不支持 Web Speech API';
    }

    // --- 图形生成逻辑 ---
    generateBtn.addEventListener('click', () => {
        const text = textInput.value.trim();
        if (text) {
            generateGraphic(text);
        }
    });

    // 支持回车键生成
    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const text = textInput.value.trim();
            if (text) {
                generateGraphic(text);
            }
        }
    });

    clearBtn.addEventListener('click', () => {
        // 保留 placeholder，移除其他所有 graphic-item
        const items = document.querySelectorAll('.graphic-item');
        items.forEach(item => item.remove());
        placeholderText.style.display = 'block';
    });

    function generateGraphic(text) {
        placeholderText.style.display = 'none';

        const item = document.createElement('div');
        item.classList.add('graphic-item');
        item.style.zIndex = zIndexCounter++;
        
        // 随机初始位置
        const maxLeft = canvasArea.clientWidth - 200;
        const maxTop = canvasArea.clientHeight - 200;
        const randomLeft = Math.max(0, Math.floor(Math.random() * maxLeft));
        const randomTop = Math.max(0, Math.floor(Math.random() * maxTop));

        item.style.left = randomLeft + 'px';
        item.style.top = randomTop + 'px';

        // 这里使用 placeholder 图片服务模拟生成
        // 实际项目中可以替换为 AI 生成接口 (如 OpenAI DALL-E)
        // 使用 placehold.co 生成带文字的图片
        const encodedText = encodeURIComponent(text);
        
        // 尝试根据关键词做一些简单的类型判断（模拟 AI 理解）
        let bgColor = 'e0e0e0';
        let textColor = '333333';
        
        if (text.includes('红')) { bgColor = 'ff0000'; textColor = 'ffffff'; }
        else if (text.includes('蓝')) { bgColor = '0000ff'; textColor = 'ffffff'; }
        else if (text.includes('绿')) { bgColor = '00ff00'; textColor = '000000'; }
        
        // 如果输入看起来像颜色，可以尝试设置为颜色块
        
        const img = document.createElement('img');
        // 使用 placehold.co 作为简单的动态图生成
        img.src = `https://placehold.co/200x200/${bgColor}/${textColor}?text=${encodedText}`;
        img.alt = text;

        const label = document.createElement('div');
        label.classList.add('label');
        label.textContent = text;

        item.appendChild(img);
        item.appendChild(label);
        canvasArea.appendChild(item);

        // 使其可拖拽
        makeDraggable(item);
    }

    // --- 拖拽功能实现 ---
    function makeDraggable(element) {
        let isDragging = false;
        let startX, startY, initialLeft, initialTop;

        element.addEventListener('mousedown', (e) => {
            isDragging = true;
            
            // 提升层级
            element.style.zIndex = zIndexCounter++;

            startX = e.clientX;
            startY = e.clientY;

            initialLeft = element.offsetLeft;
            initialTop = element.offsetTop;

            element.style.cursor = 'grabbing';
            e.preventDefault(); // 防止选中文本
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;

            const dx = e.clientX - startX;
            const dy = e.clientY - startY;

            let newLeft = initialLeft + dx;
            let newTop = initialTop + dy;

            // 边界检查
            const containerRect = canvasArea.getBoundingClientRect();
            const elemRect = element.getBoundingClientRect();

            // 简单的边界限制 (防止完全拖出)
            if (newLeft < 0) newLeft = 0;
            if (newTop < 0) newTop = 0;
            if (newLeft + element.offsetWidth > canvasArea.clientWidth) {
                newLeft = canvasArea.clientWidth - element.offsetWidth;
            }
            if (newTop + element.offsetHeight > canvasArea.clientHeight) {
                newTop = canvasArea.clientHeight - element.offsetHeight;
            }

            element.style.left = newLeft + 'px';
            element.style.top = newTop + 'px';
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                element.style.cursor = 'move';
            }
        });
    }
});
