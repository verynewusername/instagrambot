from PIL import Image, ImageDraw, ImageFont
import os
import random

class StarWarsCosmicDotGenerator:
    def __init__(self, size=1080):
        self.size = size
        self.font_cache = {}
    
    def create_cosmic_dot(self):
        """Create Star Wars style cosmic-themed image for a decimal dot"""
        # Create deep space black background like Star Wars
        img = Image.new('RGB', (self.size, self.size), (0, 0, 0))  # Pure black
        
        # Add subtle stars
        self._add_starwars_stars(img)
        
        # Add the clean white dot with Star Wars styling at decimal height
        self._draw_starwars_dot(img)
        
        return img
    
    def _add_starwars_stars(self, img):
        """Add small, bright white stars like Star Wars space scenes"""
        pixels = img.load()
        
        # Add bright white stars scattered across the black void
        num_stars = random.randint(60, 100)  # Fewer stars for that deep space feel
        
        for _ in range(num_stars):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            
            # Star Wars style stars - mostly tiny bright points
            star_type = random.choices(
                ['pinpoint', 'small', 'bright'], 
                weights=[75, 20, 5]  # Mostly tiny pinpoint stars
            )[0]
            
            if star_type == 'pinpoint':
                # Single bright pixel star
                pixels[x, y] = (255, 255, 255)  # Pure white
            
            elif star_type == 'small':
                # Small star with tiny cross
                pixels[x, y] = (255, 255, 255)
                
                # Very subtle cross arms
                if x > 0: 
                    pixels[x-1, y] = (80, 80, 80)
                if x < self.size-1: 
                    pixels[x+1, y] = (80, 80, 80)
                if y > 0: 
                    pixels[x, y-1] = (80, 80, 80)
                if y < self.size-1: 
                    pixels[x, y+1] = (80, 80, 80)
            
            elif star_type == 'bright':
                # Brighter star that stands out more
                pixels[x, y] = (255, 255, 255)
                
                # Slightly larger cross pattern
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= x+dx < self.size and 0 <= y+dy < self.size:
                            if dx == 0 and dy == 0:
                                continue  # Skip center (already set)
                            elif abs(dx) + abs(dy) == 1:  # Cross pattern only
                                pixels[x+dx, y+dy] = (120, 120, 120)
    
    def _get_starwars_font(self, size):
        """Get Star Wars style fonts with multiple fallbacks (same as digit generator)"""
        
        # Star Wars inspired font options (in order of preference)
        starwars_fonts = [
            # Official Star Wars fonts (if available)
            "StarJedi.ttf",
            "StarJediRounded.ttf",
            "StarJediOutline.ttf",
            "Aurebesh.ttf",
            
            # Sci-fi style fonts
            "Orbitron-Bold.ttf",
            "Exo-Bold.ttf",
            "Rajdhani-Bold.ttf",
            "Saira-Bold.ttf",
            
            # System fonts with futuristic feel
            "/System/Library/Fonts/Avenir Next Condensed.ttc",
            "/System/Library/Fonts/Futura.ttc",
            "/System/Library/Fonts/Impact.ttf",
            
            # Windows fonts
            "/Windows/Fonts/impact.ttf",
            "/Windows/Fonts/arial.ttf",
            
            # Linux fonts
            "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
            
            # More system fallbacks
            "Arial-Bold.ttf",
            "Helvetica-Bold.ttf",
            "arial-bold.ttf",
        ]
        
        # Try each font in order
        for font_name in starwars_fonts:
            try:
                font = ImageFont.truetype(font_name, size)
                return font
            except (OSError, IOError):
                continue
        
        # If no fonts work, use default
        return ImageFont.load_default()
    
    def _calculate_baseline_position(self):
        """Calculate where the baseline should be based on digit positioning"""
        # Use the same font sizing logic as the digit generator
        font_size = self._calculate_font_size("8", max_ratio=0.6)  # Use "8" as reference
        font = self._get_starwars_font(font_size)
        
        # Create temporary image to measure text baseline
        temp_img = Image.new('RGB', (self.size, self.size))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Get bbox for a reference digit to find baseline
        bbox = temp_draw.textbbox((0, 0), "8", font=font)
        text_height = bbox[3] - bbox[1]
        top_offset = bbox[1]
        
        # Calculate where the digit would be positioned (same as digit generator)
        digit_y = (self.size - text_height) // 2 - top_offset
        
        # The baseline is at the bottom of the text
        baseline_y = digit_y + text_height + top_offset
        
        return baseline_y, font_size
    
    def _calculate_font_size(self, text, max_ratio=0.6):
        """Calculate optimal font size (same as digit generator)"""
        target_size = int(self.size * max_ratio)
        low, high = 50, 2000
        best_size = 50
        
        while low <= high:
            mid = (low + high) // 2
            font = self._get_starwars_font(mid)
            
            temp_img = Image.new('RGB', (self.size, self.size))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            max_dimension = max(text_width, text_height)
            
            if max_dimension <= target_size:
                best_size = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return best_size
    
    def _draw_starwars_dot(self, img):
        """Draw decimal dot at proper baseline height - PERFECTLY ALIGNED"""
        draw = ImageDraw.Draw(img)
        
        # Get the baseline position based on digit positioning
        baseline_y, font_size = self._calculate_baseline_position()
        
        # Calculate dot size proportional to font size
        dot_size = max(font_size // 12, 15)  # Proportional to font, minimum 15px
        
        # Position horizontally centered, vertically at baseline
        center_x = self.size // 2
        
        # Position dot at baseline (bottom of where digits sit)
        # Move it up slightly so it sits on the baseline, not below it
        dot_y = baseline_y - dot_size
        
        dot_x = center_x - dot_size // 2
        
        # Draw a perfect circle for the decimal dot
        draw.ellipse(
            [dot_x, dot_y, dot_x + dot_size, dot_y + dot_size],
            fill=(255, 255, 255),  # Pure white
            outline=None
        )
        
        # Debug info
        print(f"Baseline Y: {baseline_y}, Dot size: {dot_size}, Dot position: ({dot_x}, {dot_y})")
    
    def generate_dot(self, output_dir="starwars_cosmic_dot"):
        """Generate Star Wars style cosmic decimal dot image"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🌌 Generating Star Wars style cosmic decimal dot...")
        print(f"📁 Output directory: {output_dir}")
        print(f"⭐ Background: Deep space black")
        print(f"🎯 Alignment: Proper decimal baseline height")
        
        print(f"✨ Creating cosmic decimal dot at baseline...")
        
        img = self.create_cosmic_dot()
        
        filename = "starwars_decimal_dot.png"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, optimize=True, quality=95)
        
        print(f"   💫 Saved {filename}")
        print(f"🎉 Successfully generated Star Wars cosmic decimal dot!")
    
    def test_dot_with_digit_alignment(self, output_dir="dot_digit_alignment_test"):
        """Test dot alignment alongside a digit to verify proper positioning"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🎯 Testing decimal dot alignment with digit reference...")
        
        # Create image with both a digit and dot for comparison
        img = Image.new('RGB', (self.size, self.size), (0, 0, 0))
        self._add_starwars_stars(img)
        
        draw = ImageDraw.Draw(img)
        
        # Draw a reference digit (like "5") on the left side
        font_size = self._calculate_font_size("5", max_ratio=0.6)
        font = self._get_starwars_font(font_size)
        
        # Position digit on left side
        bbox = draw.textbbox((0, 0), "5", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        left_offset = bbox[0]
        top_offset = bbox[1]
        
        digit_x = (self.size // 4) - (text_width // 2) - left_offset
        digit_y = (self.size - text_height) // 2 - top_offset
        
        draw.text((digit_x, digit_y), "5", font=font, fill=(255, 255, 255))
        
        # Now add the decimal dot on the right side at proper baseline
        baseline_y, _ = self._calculate_baseline_position()
        dot_size = max(font_size // 12, 15)
        
        dot_x = (3 * self.size // 4) - dot_size // 2
        dot_y = baseline_y - dot_size
        
        draw.ellipse(
            [dot_x, dot_y, dot_x + dot_size, dot_y + dot_size],
            fill=(255, 255, 255),
            outline=None
        )
        
        # Add faint baseline reference line
        draw.line([(0, baseline_y), (self.size, baseline_y)], fill=(30, 30, 30), width=1)
        
        filename = "alignment_test_digit_and_dot.png"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, optimize=True, quality=95)
        
        print("✅ Digit and dot alignment test complete! Check the alignment test folder.")
        print(f"   The dot should align with the baseline of the digit '5'")

# Usage
if __name__ == "__main__":
    generator = StarWarsCosmicDotGenerator(size=1080)
    
    # Test alignment with digit reference
    generator.test_dot_with_digit_alignment()
    
    # Generate the decimal dot at proper baseline height
    generator.generate_dot()
    
    print("\n✨ Decimal dot created at proper baseline height!")
    print("   It will align perfectly with your digits for decimal numbers!")
