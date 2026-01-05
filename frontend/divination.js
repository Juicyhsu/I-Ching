// 抽籤卜卦互動模組

class DivinationDrawer {
    constructor() {
        this.isDrawing = false;
        this.drawnNumbers = [];
    }

    // 顯示籤筒介面
    showDrawInterface(question) {
        const drawHTML = `
            <div class="divination-draw-container">
                <div class="draw-title">🔮 請誠心搖籤三次</div>
                <div class="draw-subtitle">心中默念：${question}</div>
                
                <div class="stick-and-button-wrapper">
                    <div class="stick-container">
                        ${this.createSticks()}
                    </div>
                    
                    <div class="button-area">
                        <button class="shake-btn" onclick="divinationDrawer.shakeSticks()">
                            ☯ 搖籤
                        </button>
                        <div class="draw-hint">💡 請點擊「搖籤」三次<br>每次抽出一支籤</div>
                    </div>
                </div>
                
                <div class="drawn-sticks">
                    <div class="stick-slot" data-index="0">第一籤</div>
                    <div class="stick-slot" data-index="1">第二籤</div>
                    <div class="stick-slot" data-index="2">第三籤</div>
                </div>
            </div>
        `;

        return drawHTML;
    }

    // 創建籤筒中的籤
    createSticks() {
        let sticksHTML = '';
        for (let i = 0; i < 20; i++) {
            sticksHTML += `<div class="stick" style="--delay: ${i * 0.05}s"></div>`;
        }
        return sticksHTML;
    }

    // 搖籤動畫
    async shakeSticks() {
        if (this.isDrawing) return;
        if (this.drawnNumbers.length >= 3) {
            alert('已經抽完三支籤了！');
            return;
        }

        this.isDrawing = true;
        const container = document.querySelector('.stick-container');
        const shakeBtn = document.querySelector('.shake-btn');

        // 禁用按鈕
        shakeBtn.disabled = true;
        shakeBtn.textContent = '搖籤中...';

        // 搖動動畫
        container.classList.add('shaking');

        // 等待2秒
        await this.sleep(2000);

        // 停止搖動
        container.classList.remove('shaking');

        // 抽出一支籤
        const number = Math.floor(Math.random() * 900) + 100; // 100-999
        this.drawnNumbers.push(number);

        // 顯示籤號
        const slot = document.querySelector(`.stick-slot[data-index="${this.drawnNumbers.length - 1}"]`);
        slot.innerHTML = `<div class="drawn-number">${number}</div>`;
        slot.classList.add('revealed');

        // 籤飛出動畫
        await this.animateStickOut(number, this.drawnNumbers.length - 1);

        // 恢復按鈕
        if (this.drawnNumbers.length < 3) {
            shakeBtn.disabled = false;
            shakeBtn.textContent = `☯ 搖籤 (${this.drawnNumbers.length}/3)`;
        } else {
            shakeBtn.textContent = '✓ 已完成';
            shakeBtn.classList.add('completed');

            // 1.5秒後自動送出
            setTimeout(() => {
                this.submitDivination();
            }, 1500);
        }

        this.isDrawing = false;
    }

    // 籤飛出動畫
    async animateStickOut(number, index) {
        const stick = document.createElement('div');
        stick.className = 'flying-stick';
        stick.textContent = number;
        document.querySelector('.divination-draw-container').appendChild(stick);

        await this.sleep(800);
        stick.remove();
    }

    // 送出占卜
    submitDivination() {
        // 移除抽籤介面
        const drawContainer = document.querySelector('.divination-draw-container');
        if (drawContainer) {
            drawContainer.classList.add('fade-out');
            setTimeout(() => {
                drawContainer.remove();
            }, 500);
        }

        // 調用全域回調函數，傳遞抽到的數字
        if (window.onDrawingComplete) {
            window.onDrawingComplete(this.drawnNumbers);
        }

        // 重置
        this.drawnNumbers = [];
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// 全域實例
const divinationDrawer = new DivinationDrawer();
