function searchCreature() {
    const name = document.getElementById('searchInput').value.trim();
    const resultDiv = document.getElementById('result');
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    const progress = document.createElement('div');
    progress.className = 'progress';
    progress.style.width = '0%';
    progressBar.appendChild(progress);
    const loadingText = document.createElement('div');
    loadingText.className = 'loading';
    loadingText.textContent = '正在查询，请稍候...';

    if (!name) {
        resultDiv.innerHTML = '<p class="error">请输入生物名称</p>';
        return;
    }

    // 显示加载状态和进度条
    resultDiv.innerHTML = '';
    resultDiv.appendChild(loadingText);
    resultDiv.appendChild(progressBar);

    // 模拟进度条增长（实际开发中可根据请求状态优化）
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) clearInterval(interval);
        width = Math.min(width + 10, 100); // 逐步增加进度
        progress.style.width = `${width}%`;
    }, 150);

    // 发送请求
    fetch(`/api/creature/?name=${encodeURIComponent(name)}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP错误：状态码 ${response.status}`);
            return response.json();
        })
        .then(data => {
            clearInterval(interval);
            resultDiv.innerHTML = ''; // 清空加载状态

            if (data.error) {
                resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
                return;
            }

            // 生成中文标签的HTML内容
            const html = `
                <div class="creature-info">
                    <h3>${data.name}</h3>
                    <div class="field">
                        <span class="label">名称：</span>
                        <span class="value">${data.name || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">外貌：</span>
                        <span class="value">${data.appearance || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">原始栖息地：</span>
                        <span class="value">${data.original_habitat || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">现代分布地：</span>
                        <span class="value">${data.modern_location || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">文献原文：</span>
                        <span class="value">${data.source_excerpt || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">译文：</span>
                        <span class="value">${data.source_translation || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">能力：</span>
                        <span class="value">${data.abilities || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">象征意义：</span>
                        <span class="value">${data.symbolism || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">类别：</span>
                        <span class="value">${data.category || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">山脉位置：</span>
                        <span class="value">${data.mountain_location || '无'}</span>
                    </div>
                    <div class="field">
                        <span class="label">所属章节：</span>
                        <span class="value">${data.chapter || '无'}</span>
                    </div>
                </div>
                ${data.image ? `<img class="creature-image" src="data:image/png;base64,${data.image}" alt="${data.name}">` : ''}
            `;

            resultDiv.innerHTML = html;
        })
        .catch(error => {
            clearInterval(interval);
            resultDiv.innerHTML = '<p class="error">查询失败，请重试</p>';
            console.error('请求错误：', error);
        });
}