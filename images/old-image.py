from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math
import colorsys

class InstagramNumberGenerator:
    def __init__(self, size=1080):
        self.size = size
        self.font_cache = {}
        
        # Modern color palettes
        self.color_palettes = {
            'sunset': [(255, 94, 77), (255, 154, 0), (255, 206, 84)],
            'ocean': [(64, 224, 208), (70, 130, 180), (123, 104, 238)],
            'forest': [(46, 125, 50), (102, 187, 106), (165, 214, 167)],
            'purple': [(142, 36, 170), (155, 39, 176), (186, 104, 200)],
            'pink': [(233, 30, 99), (244, 143, 177), (248, 187, 208)],
            'blue': [(33, 150, 243), (100, 181, 246), (144, 202, 249)],
            'minimal': [(45, 45, 45), (90, 90, 90), (135, 135, 135)],
            'warm': [(255, 87, 34), (255, 152, 0), (255, 193, 7)]
        }
    
    def create_image(self, number, style="gradient_modern"):
        """Create image with beautiful Instagram-ready styles"""
        styles = {
            "gradient_modern": self._create_gradient_modern,
            "neon_glow": self._create_neon_glow,
            "minimal_elegant": self._create_minimal_elegant,
            "retro_wave": self._create_retro_wave,
            "glass_morphism": self._create_glass_morphism,
            "paper_texture": self._create_paper_texture,
            "cosmic": self._create_cosmic,
            "instagram_story": self._create_instagram_story
        }
        
        return styles.get(style, self._create_gradient_modern)(number)
    
    def _create_gradient_modern(self, number):
        """Modern gradient with clean typography"""
        img = Image.new('RGB', (self.size, self.size))
        
        # Choose random palette
        import random
        palette_name = random.choice(list(self.color_palettes.keys()))
        colors = self.color_palettes[palette_name]
        
        # Create smooth gradient
        for y in range(self.size):
            for x in range(self.size):
                # Diagonal gradient with smooth transitions
                ratio = (x + y) / (2 * self.size)
                
                if ratio < 0.5:
                    # Blend first two colors
                    blend_ratio = ratio * 2
                    r = int(colors[0][0] * (1 - blend_ratio) + colors[1][0] * blend_ratio)
                    g = int(colors[0][1] * (1 - blend_ratio) + colors[1][1] * blend_ratio)
                    b = int(colors[0][2] * (1 - blend_ratio) + colors[1][2] * blend_ratio)
                else:
                    # Blend second and third colors
                    blend_ratio = (ratio - 0.5) * 2
                    r = int(colors[1][0] * (1 - blend_ratio) + colors[2][0] * blend_ratio)
                    g = int(colors[1][1] * (1 - blend_ratio) + colors[2][1] * blend_ratio)
                    b = int(colors[1][2] * (1 - blend_ratio) + colors[2][2] * blend_ratio)
                
                img.putpixel((x, y), (r, g, b))
        
        # Add subtle noise for texture
        img = self._add_noise(img, 0.02)
        
        draw = ImageDraw.Draw(img)
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.7)
        font = self._get_font(font_size, weight="bold")
        
        # Add text with shadow
        self._draw_text_with_shadow(draw, text, font, (255, 255, 255), shadow_color=(0, 0, 0, 100))
        
        return img
    
    def _create_neon_glow(self, number):
        """Neon glow effect with dark background"""
        img = Image.new('RGB', (self.size, self.size), (15, 15, 25))
        draw = ImageDraw.Draw(img)
        
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.6)
        font = self._get_font(font_size, weight="bold")
        
        # Neon colors
        neon_colors = [
            (0, 255, 255),    # Cyan
            (255, 0, 255),    # Magenta
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (255, 100, 255)   # Pink
        ]
        
        import random
        neon_color = random.choice(neon_colors)
        
        # Create glow effect with multiple layers
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.size - text_width) // 2
        y = (self.size - text_height) // 2
        
        # Glow layers (from outer to inner)
        glow_layers = [
            (20, (*neon_color, 30)),
            (15, (*neon_color, 60)),
            (10, (*neon_color, 90)),
            (5, (*neon_color, 120)),
            (2, (*neon_color, 180))
        ]
        
        for blur_radius, color in glow_layers:
            # Create temporary image for this glow layer
            temp_img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            temp_draw.text((x, y), text, font=font, fill=color)
            
            # Apply blur
            temp_img = temp_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            
            # Composite onto main image
            img = Image.alpha_composite(img.convert('RGBA'), temp_img).convert('RGB')
        
        # Final sharp text
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        return img
    
    def _create_minimal_elegant(self, number):
        """Clean minimal design with elegant typography"""
        # Soft background colors
        backgrounds = [
            (250, 250, 250),  # Off-white
            (245, 245, 247),  # Light gray
            (248, 249, 250),  # Cool white
            (253, 253, 253),  # Warm white
        ]
        
        import random
        bg_color = random.choice(backgrounds)
        
        img = Image.new('RGB', (self.size, self.size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add subtle geometric elements
        self._add_minimal_decorations(draw, bg_color)
        
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.8)
        font = self._get_font(font_size, weight="light")
        
        # Dark text for contrast
        text_color = (45, 45, 45)
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.size - text_width) // 2
        y = (self.size - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=text_color)
        
        return img
    
    def _create_retro_wave(self, number):
        """80s retro synthwave aesthetic"""
        img = Image.new('RGB', (self.size, self.size), (10, 5, 30))
        draw = ImageDraw.Draw(img)
        
        # Create retro grid background
        self._draw_retro_grid(draw)
        
        # Retro gradient sky
        for y in range(self.size // 2):
            ratio = y / (self.size // 2)
            r = int(255 * ratio + 10 * (1 - ratio))
            g = int(100 * ratio + 5 * (1 - ratio))
            b = int(200 * ratio + 30 * (1 - ratio))
            draw.line([(0, y), (self.size, y)], fill=(r, g, b))
        
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.7)
        font = self._get_font(font_size, weight="bold")
        
        # Retro colors
        retro_color = (255, 20, 147)  # Deep pink
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.size - text_width) // 2
        y = (self.size - text_height) // 2
        
        # Chrome effect
        self._draw_chrome_text(draw, text, font, x, y, retro_color)
        
        return img
    
    def _create_glass_morphism(self, number):
        """Modern glassmorphism effect"""
        # Create colorful background
        img = Image.new('RGB', (self.size, self.size))
        
        # Multiple colored circles for background
        colors = [(255, 100, 150), (100, 200, 255), (150, 255, 150), (255, 200, 100)]
        
        for i, color in enumerate(colors):
            # Create gradient circle
            circle_img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
            circle_draw = ImageDraw.Draw(circle_img)
            
            center_x = (i % 2) * self.size // 2 + self.size // 4
            center_y = (i // 2) * self.size // 2 + self.size // 4
            radius = self.size // 3
            
            circle_draw.ellipse([center_x - radius, center_y - radius, 
                               center_x + radius, center_y + radius], 
                              fill=(*color, 100))
            
            circle_img = circle_img.filter(ImageFilter.GaussianBlur(radius=50))
            img = Image.alpha_composite(img.convert('RGBA'), circle_img).convert('RGB')
        
        # Glass panel
        glass_img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        glass_draw = ImageDraw.Draw(glass_img)
        
        margin = self.size // 8
        glass_draw.rounded_rectangle([margin, margin, self.size - margin, self.size - margin],
                                   radius=30, fill=(255, 255, 255, 30),
                                   outline=(255, 255, 255, 80), width=2)
        
        img = Image.alpha_composite(img.convert('RGBA'), glass_img).convert('RGB')
        
        draw = ImageDraw.Draw(img)
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.6)
        font = self._get_font(font_size, weight="bold")
        
        self._draw_text_with_shadow(draw, text, font, (255, 255, 255), shadow_color=(0, 0, 0, 150))
        
        return img
    
    def _create_paper_texture(self, number):
        """Paper texture with letterpress effect"""
        # Cream paper background
        img = Image.new('RGB', (self.size, self.size), (252, 248, 240))
        
        # Add paper texture
        img = self._add_paper_texture(img)
        
        draw = ImageDraw.Draw(img)
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.8)
        font = self._get_font(font_size, weight="bold")
        
        # Letterpress effect
        self._draw_letterpress_text(draw, text, font)
        
        return img
    
    def _create_cosmic(self, number):
        """Cosmic space theme with stars"""
        img = Image.new('RGB', (self.size, self.size), (5, 5, 15))
        
        # Add stars
        self._add_stars(img)
        
        # Add nebula effect
        self._add_nebula(img)
        
        draw = ImageDraw.Draw(img)
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.7)
        font = self._get_font(font_size, weight="bold")
        
        # Cosmic glow
        self._draw_cosmic_text(draw, text, font)
        
        return img
    
    def _create_instagram_story(self, number):
        """Instagram story style with modern elements"""
        # Gradient background
        img = Image.new('RGB', (self.size, self.size))
        
        # Create Instagram-style gradient
        colors = [(129, 52, 175), (251, 173, 80)]  # Instagram purple to orange
        
        for y in range(self.size):
            ratio = y / self.size
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            
            for x in range(self.size):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Add decorative elements
        self._add_story_decorations(draw)
        
        text = str(number)
        font_size = self._calculate_font_size(text, max_ratio=0.8)
        font = self._get_font(font_size, weight="bold")
        
        self._draw_text_with_shadow(draw, text, font, (255, 255, 255), shadow_color=(0, 0, 0, 100))
        
        return img
    
    # Helper methods for effects
    def _add_noise(self, img, intensity=0.05):
        """Add subtle noise texture"""
        import random
        pixels = img.load()
        
        for y in range(self.size):
            for x in range(self.size):
                if random.random() < intensity:
                    r, g, b = pixels[x, y]
                    noise = random.randint(-20, 20)
                    r = max(0, min(255, r + noise))
                    g = max(0, min(255, g + noise))
                    b = max(0, min(255, b + noise))
                    pixels[x, y] = (r, g, b)
        
        return img
    
    def _add_minimal_decorations(self, draw, bg_color):
        """Add subtle geometric decorations"""
        # Light accent color
        accent = tuple(max(0, c - 20) for c in bg_color)
        
        # Corner elements
        corner_size = self.size // 20
        draw.rectangle([0, 0, corner_size, corner_size], fill=accent)
        draw.rectangle([self.size - corner_size, self.size - corner_size, 
                       self.size, self.size], fill=accent)
    
    def _draw_retro_grid(self, draw):
        """Draw retro synthwave grid"""
        grid_color = (255, 20, 147, 100)
        spacing = self.size // 20
        
        # Horizontal lines with perspective
        for i in range(self.size // 2, self.size, spacing):
            y = i
            # Perspective effect
            left_x = int((i - self.size // 2) * 0.3)
            right_x = self.size - left_x
            draw.line([(left_x, y), (right_x, y)], fill=grid_color[:3], width=2)
        
        # Vertical lines
        for i in range(spacing, self.size, spacing):
            draw.line([(i, self.size // 2), (i, self.size)], fill=grid_color[:3], width=1)
    
    def _draw_chrome_text(self, draw, text, font, x, y, base_color):
        """Draw chrome/metallic text effect"""
        # Multiple layers for chrome effect
        layers = [
            (2, 2, (0, 0, 0)),           # Shadow
            (1, 1, (100, 100, 100)),     # Dark edge
            (0, 0, (255, 255, 255)),     # Highlight
            (0, 0, base_color)           # Main color
        ]
        
        for offset_x, offset_y, color in layers:
            draw.text((x + offset_x, y + offset_y), text, font=font, fill=color)
    
    def _add_stars(self, img):
        """Add random stars to cosmic background"""
        import random
        pixels = img.load()
        
        for _ in range(200):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            brightness = random.randint(150, 255)
            pixels[x, y] = (brightness, brightness, brightness)
            
            # Add small cross pattern for brighter stars
            if brightness > 200:
                if x > 0: pixels[x-1, y] = (brightness//2, brightness//2, brightness//2)
                if x < self.size-1: pixels[x+1, y] = (brightness//2, brightness//2, brightness//2)
                if y > 0: pixels[x, y-1] = (brightness//2, brightness//2, brightness//2)
                if y < self.size-1: pixels[x, y+1] = (brightness//2, brightness//2, brightness//2)
    
    def _add_nebula(self, img):
        """Add nebula effect"""
        nebula_img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        nebula_draw = ImageDraw.Draw(nebula_img)
        
        # Multiple colored clouds
        colors = [(255, 100, 200, 30), (100, 150, 255, 30), (150, 255, 150, 30)]
        
        import random
        for color in colors:
            for _ in range(3):
                x = random.randint(0, self.size)
                y = random.randint(0, self.size)
                radius = random.randint(self.size//6, self.size//3)
                nebula_draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
        
        nebula_img = nebula_img.filter(ImageFilter.GaussianBlur(radius=30))
        img = Image.alpha_composite(img.convert('RGBA'), nebula_img).convert('RGB')
        return img
    
    def _draw_cosmic_text(self, draw, text, font):
        """Draw text with cosmic glow"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.size - text_width) // 2
        y = (self.size - text_height) // 2
        
        # Cosmic colors
        cosmic_colors = [(255, 100, 255), (100, 255, 255), (255, 255, 100)]
        import random
        glow_color = random.choice(cosmic_colors)
        
        # Glow effect
        for blur in [15, 10, 5]:
            temp_img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            temp_draw.text((x, y), text, font=font, fill=(*glow_color, 100))
            temp_img = temp_img.filter(ImageFilter.GaussianBlur(radius=blur))
            
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    def _add_story_decorations(self, draw):
        """Add Instagram story style decorations"""
        # Corner brackets
        bracket_size = self.size // 15
        bracket_width = 4
        margin = self.size // 20
        
        # Top-left bracket
        draw.line([(margin, margin), (margin + bracket_size, margin)], 
                 fill=(255, 255, 255), width=bracket_width)
        draw.line([(margin, margin), (margin, margin + bracket_size)], 
                 fill=(255, 255, 255), width=bracket_width)
        
        # Top-right bracket
        draw.line([(self.size - margin - bracket_size, margin), (self.size - margin, margin)], 
                 fill=(255, 255, 255), width=bracket_width)
        draw.line([(self.size - margin, margin), (self.size - margin, margin + bracket_size)], 
                 fill=(255, 255, 255), width=bracket_width)
        
        # Bottom-left bracket
        draw.line([(margin, self.size - margin - bracket_size), (margin, self.size - margin)], 
                 fill=(255, 255, 255), width=bracket_width)
        draw.line([(margin, self.size - margin), (margin + bracket_size, self.size - margin)], 
                 fill=(255, 255, 255), width=bracket_width)
        
        # Bottom-right bracket
        draw.line([(self.size - margin, self.size - margin - bracket_size), 
                  (self.size - margin, self.size - margin)], 
                 fill=(255, 255, 255), width=bracket_width)
        draw.line([(self.size - margin - bracket_size, self.size - margin), 
                  (self.size - margin, self.size - margin)], 
                 fill=(255, 255, 255), width=bracket_width)
    
    def _add_paper_texture(self, img):
        """Add paper texture"""
        import random
        pixels = img.load()
        
        for y in range(self.size):
            for x in range(self.size):
                if random.random() < 0.1:
                    r, g, b = pixels[x, y]
                    variation = random.randint(-5, 5)
                    r = max(0, min(255, r + variation))
                    g = max(0, min(255, g + variation))
                    b = max(0, min(255, b + variation))
                    pixels[x, y] = (r, g, b)
        
        return img
    
    def _draw_letterpress_text(self, draw, text, font):
        """Draw letterpress effect text"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.size - text_width) // 2
        y = (self.size - text_height) // 2
        
        # Embossed effect
        draw.text((x + 2, y + 2), text, font=font, fill=(200, 200, 200))  # Shadow
        draw.text((x - 1, y - 1), text, font=font, fill=(255, 255, 255))  # Highlight
        draw.text((x, y), text, font=font, fill=(80, 80, 80))  # Main text
    
    def _draw_text_with_shadow(self, draw, text, font, text_color, shadow_color=(0, 0, 0, 100)):
        """Draw text with shadow"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.size - text_width) // 2
        y = (self.size - text_height) // 2
        
        # Shadow
        shadow_offset = max(2, len(str(text)) // 3)
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color[:3])
        
        # Main text
        draw.text((x, y), text, font=font, fill=text_color)
    
    def _calculate_font_size(self, text, max_ratio=0.8):
        """Calculate optimal font size with caching"""
        text_length = len(text)
        cache_key = f"{text_length}_{max_ratio}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        target_size = int(self.size * max_ratio)
        low, high = 1, 1000
        best_size = 1
        
        while low <= high:
            mid = (low + high) // 2
            font = self._get_font(mid)
            
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if text_width <= target_size and text_height <= target_size:
                best_size = mid
                low = mid + 1
            else:
                high = mid - 1
        
        self.font_cache[cache_key] = best_size
        return best_size
    
    def _get_font(self, size, weight="regular"):
        """Get font with different weights"""
        font_paths = {
            "bold": [
                "arial-bold.ttf", "Arial-Bold.ttf", 
                "/System/Library/Fonts/Arial Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ],
            "light": [
                "arial-light.ttf", "Arial-Light.ttf",
                "/System/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ],
            "regular": [
                "arial.ttf", "Arial.ttf",
                "/System/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ]
        }
        
        for font_path in font_paths.get(weight, font_paths["regular"]):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
        
        return ImageFont.load_default()
    
    def generate_batch(self, start_number, count, output_dir="instagram_posts", style="gradient_modern"):
        """Generate batch with progress tracking"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🎨 Generating {count} beautiful Instagram posts...")
        print(f"📁 Output directory: {output_dir}")
        print(f"🎭 Style: {style}")
        print(f"📊 Starting from number: {start_number:,}")
        
        for i in range(count):
            number = start_number + i
            img = self.create_image(number, style)
            
            filename = f"post_{number:012d}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, optimize=True, quality=95)
            
            # Progress indicator
            if i % 100 == 0 or i == count - 1:
                progress = (i + 1) / count * 100
                print(f"✨ Progress: {progress:.1f}% ({i+1:,}/{count:,} images)")
        
        print(f"🎉 Successfully generated {count:,} images!")

# Usage examples
if __name__ == "__main__":
    generator = InstagramNumberGenerator()
    
    # Available styles:
    styles = [
        "gradient_modern",    # Modern gradients with clean typography
        "neon_glow",         # Cyberpunk neon glow effect
        "minimal_elegant",   # Clean minimal design
        "retro_wave",        # 80s synthwave aesthetic
        "glass_morphism",    # Modern glassmorphism
        "paper_texture",     # Vintage paper with letterpress
        "cosmic",            # Space theme with stars
        "instagram_story"    # Instagram story style
    ]
    
    # Generate samples of each style
    print("🎨 Creating sample images for each style...")
    for style in styles:
        img = generator.create_image(12345, style)
        img.save(f"sample_{style}.png")
        print(f"✅ Created sample_{style}.png")
    
    # Generate a batch with your preferred style
    generator.generate_batch(
        start_number=1,
        count=1000,
        output_dir="beautiful_instagram_posts",
        style="gradient_modern"  # Change this to your preferred style
    )
    
    # Test with large numbers
    test_numbers = [999999, 1000000, 999999999, 1000000000]
    for num in test_numbers:
        img = generator.create_image(num, "neon_glow")
        img.save(f"test_large_{num}.png")
        print(f"✅ Created test image for {num:,}")
