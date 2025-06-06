from PIL import Image, ImageDraw, ImageFont
import os
import random

class StarWarsCosmicDigitGenerator:
    def __init__(self, size=1080):
        self.size = size
        self.font_cache = {}
    
    def create_cosmic_digit(self, digit):
        """Create Star Wars style cosmic-themed image for a single digit (0-9)"""
        if not (0 <= digit <= 9):
            raise ValueError("Digit must be between 0 and 9")
        
        # Create deep space black background like Star Wars
        img = Image.new('RGB', (self.size, self.size), (0, 0, 0))  # Pure black
        
        # Add subtle stars
        self._add_starwars_stars(img)
        
        # Add the clean white digit with Star Wars font
        self._draw_starwars_digit(img, str(digit))
        
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
    
    def _draw_starwars_digit(self, img, digit):
        """Draw digit with Star Wars style font - PERFECTLY CENTERED"""
        draw = ImageDraw.Draw(img)
        
        # Calculate font size to fill most of the image
        font_size = self._calculate_font_size(digit, max_ratio=0.6)
        font = self._get_starwars_font(font_size)
        
        # Get ACCURATE text dimensions using textbbox
        bbox = draw.textbbox((0, 0), digit, font=font)
        
        # Calculate actual text dimensions
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate offsets from the bbox
        left_offset = bbox[0]
        top_offset = bbox[1]
        
        # Calculate perfect center position accounting for font metrics
        x = (self.size - text_width) // 2 - left_offset
        y = (self.size - text_height) // 2 - top_offset
        
        # Draw pure white digit on black background
        draw.text((x, y), digit, font=font, fill=(255, 255, 255))
        
        # Debug info (optional - remove in production)
        print(f"Digit: {digit}, Font size: {font_size}, Position: ({x}, {y}), Size: {text_width}x{text_height}")
    
    def _get_starwars_font(self, size):
        """Get Star Wars style fonts with multiple fallbacks"""
        
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
    
    def _calculate_font_size(self, text, max_ratio=0.6):
        """Calculate optimal font size with proper centering"""
        target_size = int(self.size * max_ratio)
        low, high = 50, 2000  # Start with reasonable minimum
        best_size = 50
        
        while low <= high:
            mid = (low + high) // 2
            font = self._get_starwars_font(mid)
            
            # Create temporary image to measure text
            temp_img = Image.new('RGB', (self.size, self.size))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Use the larger dimension to ensure it fits
            max_dimension = max(text_width, text_height)
            
            if max_dimension <= target_size:
                best_size = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return best_size
    
    def generate_all_digits(self, output_dir="starwars_cosmic_digits"):
        """Generate Star Wars style cosmic images for all digits 0-9"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🌌 Generating Star Wars style cosmic digit images...")
        print(f"📁 Output directory: {output_dir}")
        print(f"⭐ Background: Deep space black")
        print(f"🎭 Font: Star Wars inspired typography")
        print(f"🎯 Alignment: Perfect centering")
        
        for digit in range(10):
            print(f"✨ Creating cosmic digit {digit}...")
            
            img = self.create_cosmic_digit(digit)
            
            filename = f"starwars_digit_{digit}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, optimize=True, quality=95)
            
            print(f"   💫 Saved {filename}")
        
        print(f"🎉 Successfully generated all Star Wars cosmic digit images!")
        print(f"📊 Total files created: 10 (digits 0-9)")
    
    def generate_number_sequence(self, number, output_dir="starwars_cosmic_numbers"):
        """Generate image for a multi-digit number with perfect alignment"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Create image with pure black background
        img = Image.new('RGB', (self.size, self.size), (0, 0, 0))
        self._add_starwars_stars(img)
        
        draw = ImageDraw.Draw(img)
        text = str(number)
        
        # Calculate font size for the full number
        font_size = self._calculate_font_size(text, max_ratio=0.5)
        font = self._get_starwars_font(font_size)
        
        # Get accurate text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        left_offset = bbox[0]
        top_offset = bbox[1]
        
        # Perfect center calculation
        x = (self.size - text_width) // 2 - left_offset
        y = (self.size - text_height) // 2 - top_offset
        
        # Draw the number in pure white
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        # Save the image
        filename = f"starwars_number_{number}.png"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, optimize=True, quality=95)
        
        print(f"✅ Created {filename} - Position: ({x}, {y})")
        return img
    
    def test_alignment(self, output_dir="alignment_test"):
        """Test alignment with all digits to ensure consistency"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🎯 Testing alignment for all digits...")
        
        for digit in range(10):
            img = self.create_cosmic_digit(digit)
            
            # Add alignment guides (optional - for testing)
            draw = ImageDraw.Draw(img)
            center = self.size // 2
            
            # Draw center crosshairs (very faint)
            draw.line([(center - 50, center), (center + 50, center)], fill=(50, 50, 50), width=1)
            draw.line([(center, center - 50), (center, center + 50)], fill=(50, 50, 50), width=1)
            
            filename = f"alignment_test_digit_{digit}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, optimize=True, quality=95)
        
        print("✅ Alignment test complete! Check the alignment_test folder.")

# Usage
if __name__ == "__main__":
    generator = StarWarsCosmicDigitGenerator(size=1080)
    
    # Test alignment first
    generator.test_alignment()
    
    # Generate all individual digits 0-9 with perfect alignment
    generator.generate_all_digits()
    
    # Generate some example numbers
    print("\n🌟 Creating sample numbers with perfect alignment...")
    sample_numbers = [12345, 0, 1, 23, 456, 7890]
    
    for number in sample_numbers:
        generator.generate_number_sequence(number)
    
    print("\n✨ All done! Numbers should now be perfectly centered!")
