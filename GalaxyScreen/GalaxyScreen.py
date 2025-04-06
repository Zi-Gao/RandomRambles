import pygame
import sys
import math
import random
import datetime
from pygame import gfxdraw
from collections import deque

# 配置参数
WIN_WIDTH, WIN_HEIGHT = 1920, 1080
FPS = 60
G = 800
EPSILON = 10.0
TRAIL_LENGTH = 100
BACKGROUND_COLOR = (15, 15, 25)
BODY_COLORS = [
    (255, 105, 180),  # 粉红
    (123, 104, 238),  # 暗紫罗兰
    (70, 130, 180),   # 钢蓝
    (72, 209, 204),   # 绿松石
    (60, 179, 113)    # 海洋绿
]
MAX_ZOOM_OUT = 0.5
SPAWN_RADIUS = 200  # 生成半径（世界坐标）

MASS_RANGES = {
    pygame.K_0: (1, 100),
    pygame.K_1: (100, 500),
    pygame.K_2: (500, 1000),
    pygame.K_3: (1000, 2000),
    pygame.K_4: (2000, 5000),
    pygame.K_5: (5000, 10000),
    pygame.K_6: (10000, 20000),
    pygame.K_7: (20000, 50000),
    pygame.K_8: (50000, 100000),
    pygame.K_9: (100000, 200000)
}

class CelestialBody:
    def __init__(self, mass, density, x, y, vx, vy, color, lmass, rmass):
        self.mass = mass
        self.density = density
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lmass = lmass
        self.rmass = rmass
        self.color = color
        self.radius = max(3, (3 * mass / (4 * math.pi * density)) ** (1/3))
        self.trail = deque(maxlen=TRAIL_LENGTH)
        self.halo_alpha = 90

    def update_position(self, dt, wrap_mode, screen_width, screen_height):
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        if wrap_mode:
            self.x %= screen_width
            self.y %= screen_height
        
        self.trail.append((self.x, self.y))

def generate_new_body(camera, screen_width, screen_height, wrap_mode, bodies, color_index, lmass, rmass):
    """在质量中心附近生成新天体"""
    if wrap_mode or not bodies:
        # 环绕模式或没有天体时在屏幕中心生成
        world_center_x = screen_width/2
        world_center_y = screen_height/2
    else:
        # 计算质量中心
        total_mass = sum(b.mass for b in bodies)
        world_center_x = sum(b.x * b.mass for b in bodies) / total_mass
        world_center_y = sum(b.y * b.mass for b in bodies) / total_mass
    
    # 在质量中心附近生成
    offset = SPAWN_RADIUS * (1 + random.random())  # 随机偏移
    angle = random.uniform(0, 2*math.pi)
    x = world_center_x + math.cos(angle) * offset
    y = world_center_y + math.sin(angle) * offset

    mass = random.uniform(lmass, rmass)
    density = random.uniform(0.3, 1.8)
    speed = random.uniform(0.1, 0.6) * (1 + mass/200)
    
    return CelestialBody(
        mass=mass,
        density=density,
        x=x,
        y=y,
        vx=math.cos(angle+math.pi/2) * speed,
        vy=math.sin(angle+math.pi/2) * speed,
        color=BODY_COLORS[color_index % len(BODY_COLORS)],
        lmass=lmass,
        rmass=rmass,
    )

def compute_forces(bodies):
    forces = [[] for _ in bodies]
    for i, body in enumerate(bodies):
        fx, fy = 0, 0
        for j, other in enumerate(bodies):
            if i != j:
                dx = other.x - body.x
                dy = other.y - body.y
                r_sq = dx**2 + dy**2 + EPSILON**2
                r = math.sqrt(r_sq)
                f = G * body.mass * other.mass / r_sq
                fx += f * dx / r
                fy += f * dy / r
        forces[i] = (fx/body.mass, fy/body.mass)
    return forces

class SmoothCamera:
    def __init__(self, screen_width, screen_height):
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.center = (screen_width/2, screen_height/2)
        self.target_center = (screen_width/2, screen_height/2)
    
    def update(self, bodies, wrap_mode, screen_width, screen_height):
        if wrap_mode or not bodies:
            return
        
        min_x = min(b.x for b in bodies)
        max_x = max(b.x for b in bodies)
        min_y = min(b.y for b in bodies)
        max_y = max(b.y for b in bodies)
        
        self.target_center = ((min_x + max_x)/2, (min_y + max_y)/2)
        area_width = max(max_x - min_x, 200) + 400
        area_height = max(max_y - min_y, 200) + 400
        self.target_zoom = min(screen_width/area_width, screen_height/area_height)
        
        self.zoom = self.zoom * 0.95 + self.target_zoom * 0.05
        self.center = (
            self.center[0] * 0.95 + self.target_center[0] * 0.05,
            self.center[1] * 0.95 + self.target_center[1] * 0.05
        )

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.Font("font.ttc", 20)
    except:
        font = pygame.font.SysFont("simhei", 20)
    
    fullscreen_mode = False
    wrap_mode = False
    show_help = True
    bodies = []
    camera = SmoothCamera(WIN_WIDTH, WIN_HEIGHT)
    color_index = 0



    while True:
        current_width, current_height = screen.get_size()
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_w:
                    wrap_mode = not wrap_mode
                elif event.key == pygame.K_h:
                    show_help = not show_help
                elif event.key == pygame.K_f:
                    fullscreen_mode = not fullscreen_mode
                    if fullscreen_mode:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
                elif event.key in MASS_RANGES:  # 数字键处理
                    lmass, rmass = MASS_RANGES[event.key]
                    new_body = generate_new_body(camera, current_width, current_height, wrap_mode, bodies, color_index, lmass, rmass)
                    bodies.append(new_body)
                    color_index += 1
                elif event.key == pygame.K_BACKSPACE and bodies:
                    color_counts = {}
                    for body in bodies:
                        color_counts[body.color] = color_counts.get(body.color, 0) + 1
                    max_count = max(color_counts.values())
                    max_colors = [color for color, count in color_counts.items() if count == max_count]
                    target_color = random.choice(max_colors)
                    candidates = [b for b in bodies if b.color == target_color]
                    if candidates:
                        bodies.remove(random.choice(candidates))
            
            if event.type == pygame.VIDEORESIZE and not fullscreen_mode:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        dt = clock.tick(FPS) * 0.001

        # 物理计算
        if bodies:
            forces = compute_forces(bodies)
            for i, body in enumerate(bodies):
                ax, ay = forces[i]
                body.vx += ax * dt
                body.vy += ay * dt
                body.update_position(dt, wrap_mode, current_width, current_height)

        # 自动天体管理
        if bodies and not wrap_mode and camera.zoom < MAX_ZOOM_OUT and len(bodies) > 1:
            # 计算质量中心
            total_mass = sum(b.mass for b in bodies)
            mass_center_x = sum(b.x * b.mass for b in bodies) / total_mass
            mass_center_y = sum(b.y * b.mass for b in bodies) / total_mass
            
            # 找到距离质量中心最远的天体
            farthest = max(bodies, key=lambda b: math.hypot(b.x-mass_center_x, b.y-mass_center_y))
            lmass=farthest.lmass
            rmass=farthest.rmass
            
            bodies.remove(farthest)
            # 在质量中心附近生成新天体
            new_body = generate_new_body(camera, current_width, current_height, wrap_mode, bodies, color_index, lmass, rmass)
            bodies.append(new_body)
            color_index += 1

        # 更新摄像机
        camera.update(bodies, wrap_mode, current_width, current_height)

        # 绘制场景
        screen.fill(BACKGROUND_COLOR)
        
        # 新轨迹效果
        for body in bodies:
            trail_length = len(body.trail)
            for idx, pos in enumerate(body.trail):
                if trail_length == 0:
                    continue
                # 新透明度公式：alpha = 100 * (idx/(2*trail_length))^2
                progress = idx / (trail_length * 2)
                alpha = int(100 * (progress ** 2))
                
                tx, ty = pos
                if not wrap_mode:
                    tx = (tx - camera.center[0]) * camera.zoom + current_width/2
                    ty = (ty - camera.center[1]) * camera.zoom + current_height/2
                if 0 <= tx <= current_width and 0 <= ty <= current_height:
                    gfxdraw.filled_circle(screen, int(tx), int(ty), 1, (*body.color, alpha))
                    gfxdraw.aacircle(screen, int(tx), int(ty), 1, (*body.color, alpha))

        # 绘制天体（保持原有光晕效果）
        for body in bodies:
            if wrap_mode:
                sx, sy = body.x, body.y
                radius = body.radius
            else:
                sx = (body.x - camera.center[0]) * camera.zoom + current_width/2
                sy = (body.y - camera.center[1]) * camera.zoom + current_height/2
                radius = body.radius * camera.zoom
            
            # 光晕效果
            num_halo = 50
            halo_radius = radius
            for i in range(num_halo, 0, -1):
                alpha = radius**2 / halo_radius**2
                halo_radius += radius / num_halo * 3
                halo_surf = pygame.Surface((halo_radius*2, halo_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(halo_surf, (*body.color, int(10*alpha)), 
                                 (halo_radius, halo_radius), halo_radius)
                screen.blit(halo_surf, (sx - halo_radius, sy - halo_radius))
            
            gfxdraw.filled_circle(screen, int(sx), int(sy), int(radius), body.color)
            gfxdraw.aacircle(screen, int(sx), int(sy), int(radius), body.color)

        # 时间显示
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        screen.blit(font.render(time_str, True, (200,200,200)), (10, current_height-40))

        # 帮助信息
        if show_help:
            help_texts = [
                "空格: 质量中心添加",
                "退格: 删除最多颜色",
                "W: 环绕模式",
                "F: 全屏切换",
                "H: 隐藏帮助",
                f"天体数量: {len(bodies)}",
                f"颜色轮换: {BODY_COLORS[color_index%len(BODY_COLORS)]}",
                f"模式: {'环绕' if wrap_mode else '自由'}",
                f"缩放: {camera.zoom:.2f}x",
                f"全屏: {'是' if fullscreen_mode else '否'}"
            ]
            y_pos = 10
            for text in help_texts:
                screen.blit(font.render(text, True, (200,200,200)), (10, y_pos))
                y_pos += 25

        pygame.display.flip()

if __name__ == "__main__":
    main()