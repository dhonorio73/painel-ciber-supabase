<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Douglas Honório | Portfólio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', Courier, monospace;
        }
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            overflow-x: hidden;
        }
        canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
        .container {
            max-width: 900px;
            margin: 50px auto;
            padding: 30px;
            background: rgba(13, 17, 23, 0.85);
            border: 1px solid #30363d;
            border-radius: 8px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }
        header h1 {
            color: #58a6ff;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        header p {
            color: #8b949e;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }
        section {
            margin-top: 30px;
        }
        h2 {
            color: #58a6ff;
            border-bottom: 1px solid #30363d;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        li {
            padding: 8px 0;
            border-bottom: 1px dashed #21262d;
        }
        a {
            color: #58a6ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

    <canvas id="matrix-canvas"></canvas>

    <div class="container">
        <header>
            <h1>Douglas Honório</h1>
            <p>Desenvolvedor Backend & Cibersegurança</p>
        </header>

        <section>
            <h2>Sobre Mim</h2>
            <p>Estudante de Cibersegurança na Faculdade Anhanguera, focado em desenvolvimento backend, criptografia, automação com Python e análise de dados defensivos.</p>
        </section>

        <section>
            <h2>Tecnologias & Ferramentas</h2>
            <ul>
                <li><strong>Linguagens:</strong> Python (Flask, Streamlit, Pandas, Scikit-Learn)</li>
                <li><strong>Segurança:</strong> Criptografia Fernet, SHA-256, Hashlib</li>
                <li><strong>Base de Dados:</strong> Supabase, PostgreSQL, Normalização (1FN/2FN)</li>
                <li><strong>Controlo de Versão:</strong> Git & GitHub</li>
            </ul>
        </section>

        <section>
            <h2>Projetos em Destaque</h2>
            <ul>
                <li><a href="https://painel-ciber-supabase-lgeyn7zzphlichhycpfqkb.streamlit.app/" target="_blank">Painel de Observabilidade e Cibersegurança (Streamlit)</a></li>
            </ul>
        </section>
    </div>

    <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const letters = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*';
        const fontSize = 16;
        let columns = canvas.width / fontSize;
        const drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(13, 17, 23, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00ff66';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 35);
    </script>
</body>
</html>
