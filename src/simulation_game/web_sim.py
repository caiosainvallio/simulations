def get_simulation_html(population_size=200, beta=0.5, gamma=0.1, initial_i=0.05):
    """
    Returns a string containing the full HTML/JS for the physics simulation.
    
    Args:
        population_size: Total number of particles.
        beta: Infection probability per contact (0.0 to 1.0).
        gamma: Recovery rate (controls duration).
        initial_i: Proportion of initial infected.
    """
    
    # Map gamma to recovery frames at 60fps
    # Duration ~ 1/gamma days. Let's say 1 day in Sim = 60 frames (1 sec).
    # So duration_frames = (1/gamma) * 60
    # Avoid division by zero
    g = max(0.001, gamma)
    recovery_frames = int((1.0 / g) * 60)
    
    # Map beta to transmission probability per collision
    # Beta is rate per time/contact. Here we just use it as probability 0-1.
    transmission_prob = min(1.0, max(0.0, beta))

    initial_infected_count = int(population_size * initial_i)
    if initial_infected_count < 1: initial_infected_count = 1

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #202025; color: white; font-family: sans-serif; }}
        canvas {{ display: block; margin: 0 auto; }}
        #stats {{ position: absolute; top: 10px; left: 10px; pointer-events: none; }}
    </style>
    </head>
    <body>
    <div id="stats">
        <div>Susceptible: <span id="val_s" style="color:#4dabf5">0</span></div>
        <div>Infected: <span id="val_i" style="color:#f44336">0</span></div>
        <div>Recovered: <span id="val_r" style="color:#66bb6a">0</span></div>
    </div>
    <canvas id="simCanvas"></canvas>
    
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        
        // Configuration injected from Python
        const POP_SIZE = {population_size};
        const TRANS_PROB = {transmission_prob};
        const RECOVERY_FRAMES = {recovery_frames};
        const INIT_INFECTED = {initial_infected_count};
        
        let width, height;
        
        function resize() {{
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
        }}
        window.addEventListener('resize', resize);
        resize();
        
        // Particle Class
        class Particle {{
            constructor(state) {{
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                const angle = Math.random() * Math.PI * 2;
                const speed = 2 + Math.random();
                this.vx = Math.cos(angle) * speed;
                this.vy = Math.sin(angle) * speed;
                this.radius = 5;
                this.state = state; // 0=S, 1=I, 2=R
                this.timer = 0;
            }}
            
            update() {{
                this.x += this.vx;
                this.y += this.vy;
                
                // Bounce
                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;
                
                // Clamp
                this.x = Math.max(0, Math.min(width, this.x));
                this.y = Math.max(0, Math.min(height, this.y));
                
                // Recovery
                if (this.state === 1) {{
                    this.timer++;
                    if (this.timer > RECOVERY_FRAMES) {{
                        stateChange(this, 2);
                    }}
                }}
            }}
            
            draw() {{
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                if (this.state === 0) ctx.fillStyle = '#4dabf5'; // S Blue
                else if (this.state === 1) ctx.fillStyle = '#f44336'; // I Red
                else ctx.fillStyle = '#66bb6a'; // R Green
                ctx.fill();
                ctx.closePath();
            }}
        }}
        
        const particles = [];
        
        function init() {{
            for (let i = 0; i < POP_SIZE; i++) {{
                let state = 0; // S
                if (i < INIT_INFECTED) state = 1; // I
                particles.push(new Particle(state));
            }}
        }}

        function stateChange(p, newState) {{
            p.state = newState;
        }}

        function checkCollisions() {{
            for (let i = 0; i < particles.length; i++) {{
                for (let j = i + 1; j < particles.length; j++) {{
                    const p1 = particles[i];
                    const p2 = particles[j];
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const distSq = dx*dx + dy*dy;
                    
                    if (distSq < 4 * 25) {{ // 2 * radius squared (r=5 -> 10^2 = 100)
                        // Collision Response (Elastic-ish)
                        // Just swap velocities for simplicity
                        const tempVx = p1.vx;
                        const tempVy = p1.vy;
                        p1.vx = p2.vx;
                        p1.vy = p2.vy;
                        p2.vx = tempVx;
                        p2.vy = tempVy;
                        
                        // Push apart to prevent sticking
                        const dist = Math.sqrt(distSq);
                        const overlap = 10 - dist;
                        if (dist > 0) {{
                            const nx = dx / dist;
                            const ny = dy / dist;
                            p1.x += nx * overlap * 0.5;
                            p1.y += ny * overlap * 0.5;
                            p2.x -= nx * overlap * 0.5;
                            p2.y -= ny * overlap * 0.5;
                        }}
                        
                        // Infection
                        if (p1.state === 1 && p2.state === 0) {{
                             if (Math.random() < TRANS_PROB) stateChange(p2, 1);
                        }} else if (p1.state === 0 && p2.state === 1) {{
                             if (Math.random() < TRANS_PROB) stateChange(p1, 1);
                        }}
                    }}
                }}
            }}
        }}
        
        function loop() {{
            ctx.clearRect(0, 0, width, height);
            
            let s = 0, i_count = 0, r = 0;
            
            checkCollisions();
            
            for (let p of particles) {{
                p.update();
                p.draw();
                
                if (p.state === 0) s++;
                else if (p.state === 1) i_count++;
                else r++;
            }}
            
            // Update stats
            document.getElementById('val_s').innerText = s;
            document.getElementById('val_i').innerText = i_count;
            document.getElementById('val_r').innerText = r;
            
            requestAnimationFrame(loop);
        }}
        
        init();
        loop();
        
    </script>
    </body>
    </html>
    """
    return html
