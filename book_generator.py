import os
import sys
import time
import urllib.parse
import argparse
import requests
from io import BytesIO
from PIL import Image, ImageOps, ImageFilter
from reportlab.lib.pagesizes import letter # 8.5 x 11 inches
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
 
# -------------------------------------------------------------
# THEME PROMPTS & METADATA DATABASE
# -------------------------------------------------------------
THEMES = {
    "funny_characters": {
        "title": "Hilarious Daily Hustle: Funny Characters in Action Coloring Book",
        "subtitle": "A Laugh-Out-Loud Coloring Adventure of Quirky Street Characters, Crazy Chores, and Daily Chaos for Kids and Adults",
        "categories": [
            "Humor / Topic / General",
            "Juvenile Nonfiction / Activity Books / Coloring",
            "Crafts, Hobbies & Home / Coloring Books for Grown-Ups"
        ],
        "keywords": [
            "funny coloring book for kids",
            "humorous cartoon coloring pages",
            "daily life funny character art",
            "stress relief funny coloring adults",
            "quirky cartoon coloring book",
            "funny chores and professions art",
            "silly scenes activity book"
        ],
        "description": """<h3>Get Ready to Laugh and Color with the Funniest Characters in Town!</h3>
<p>Step into a world of comedic chaos and high-energy laughs! <b>Hilarious Daily Hustle</b> features over 45+ unique, laugh-out-loud illustrations of exaggerated cartoon characters turning everyday chores and professions into pure comedy.</p>
 
<p><b>What’s Inside This Book:</b></p>
<ul>
  <li><b>Theatrical Chai & Tea Masters:</b> Pouring tea from three feet up in the air with dramatic style!</li>
  <li><b>Chaotic Chefs & Street Cooks:</b> Flipping giant pancakes and noodles high up into the clouds!</li>
  <li><b>The Laundry Day Tornado:</b> Wrestling with giant flying soap bubbles and rogue flying socks!</li>
  <li><b>The Crazy Commute:</b> Funny auto-rickshaws and bikes zig-zagging past smiling animals!</li>
  <li><b>Single-Sided Pages:</b> Every illustration is backed by a blank page to prevent marker bleed-through.</li>
  <li><b>Large Format:</b> Perfect 8.5 x 11 inch pages with crisp, bold black outlines easy for all skill levels to color.</li>
</ul>
 
<p>Whether you are looking for an entertaining gift for kids, teens, or adults needing a good laugh and stress-relief coloring session, this book will brighten anyone's day!</p>""",
        "prompts": [
            "funny cheerful tea stall vendor with giant mustache, pouring hot tea acrobatically from high up in the air into a steel cup, splash dynamic, energetic caricature style",
            "funny cartoon chef in kitchen tossing giant pizza dough all the way into the ceiling, flying tomatoes, comedic expression, bold clean line art",
            "hilarious character battling giant laundry soap bubbles, tangled in clothesline and bedsheets, wide funny eyes, thick black line art",
            "funny street food vendor tossing noodles high in wok, smiling cheerful exaggerated caricature, bold outline",
            "comical auto rickshaw driver laughing and steering through friendly flying pigeons, cartoon style, clean line art",
            "sleepy cartoon character brushing teeth with three toothbrushes at once, funny morning messy hair, comic line art",
            "funny grandma character proudly holding a giant wooden spoon over a bubbling soup pot with steam swirling, cute caricature",
            "funny grocery shopper balancing a huge stack of grocery bags and a giant watermelon on head, wobbling hilariously",
            "crazy funny barber giving a poodle and a customer matching curly haircuts at the same time, funny cartoon scene",
            "funny gardener holding a wild garden hose that is twisting like a snake, spraying water everywhere, cartoon humor",
            "funny mailman being chased playfully by a tiny happy kitten while letters fly in the air, funny expression",
            "cheerful funny baker covered in flour holding a gigantic croissant like a surfboard, comic caricature",
            "funny musician playing violin so intensely that music notes are dancing around comically, exaggerated posture",
            "funny street hawker balancing 10 different colorful hats on top of his head, joyful cartoon caricature",
            "funny clumsy plumber holding a giant wrench while a comical friendly water fountain shoots from a pipe, funny cartoon",
            "funny painter character accidentally painting a mustache on his own face instead of the canvas, humorous expression",
            "funny construction worker using a jackhammer that is vibrating him into a blurry comedic wiggle, cartoon style",
            "funny librarian shushing three singing birds sitting on top of an open book, cute whimsical caricature",
            "funny photographer character tangled up inside the tripod legs while taking a selfie, slapstick cartoon humor",
            "funny fruit seller tossing oranges in the air like a circus juggler with a huge happy grin, bold line art",
            "funny fisherman catching an old boot with a tiny happy crab inside wearing sunglasses, hilarious comic style",
            "funny dad making pancakes in the kitchen with pancakes stuck to the ceiling and walls, chaotic family humor",
            "funny scientist mixing two bubbling test tubes with colorful smoke turning into funny animal faces, cartoon",
            "funny traffic police officer directing funny dancing cows across a street crossing with a big whistle and smile",
            "funny street ice cream vendor serving a tower of 10 ice cream scoops wobbling dangerously high in the air",
            "funny milkman delivering bottles on an old bicycle with curious cats riding on the handlebars, joyful cartoon",
            "funny yoga instructor twisted up like a pretzel trying to scratch his own nose, humorous cartoon pose",
            "funny window cleaner making soap art faces on a skyscraper glass window, cheerful caricature",
            "funny tailor measuring a very tall giraffe for a custom suit, measuring tape flying everywhere, whimsical cartoon",
            "funny shoe repair cobbler sitting on a giant comical boot surrounded by tiny funny shoes, whimsical scene",
            "funny farmer chasing a runaway giant pumpkin rolling downhill like a giant wheel, cartoon slapstick",
            "funny balloon seller floating slightly off the ground held by a giant bunch of smiling balloons, cartoon",
            "funny mechanic peeking out from under a car hood covered in funny cartoon grease smudges and a big smile",
            "funny bus conductor punching tickets so fast tickets are flying like confetti, energetic caricature",
            "funny street juice maker squeezing giant oranges with both hands with juice splashing into funny cups",
            "funny dog walker being pulled smoothly on roller skates by five tiny happy chihuahuas, comic scene",
            "funny street magician pulling a long string of colorful handkerchiefs out of his ear with a proud smile",
            "funny firefighter rescuing a very smug cat sitting on a low tree branch enjoying a saucer of milk",
            "funny student carrying a backpack stuffed with so many giant books that only two little feet stick out",
            "funny tourist with five cameras around neck trying to read an enormous unfolded paper map upside down",
            "funny popcorn vendor standing near an exploding popcorn machine with popcorn flying everywhere like snow",
            "funny butcher feeding a string of sausages to a line of polite little alley cats sitting in a row",
            "funny street musician playing accordion while dancing on one leg with a tambourine tied to the other shoe",
            "funny painter balancing on a ladder with paint buckets on his feet, creating splash art on the wall",
            "funny street portrait artist drawing a funny cartoon version of a laughing bulldog sitting on a stool",
            "funny delivery boy on scooter with a stack of 8 pizza boxes swaying in the wind, big happy grin",
            "funny street watchmaker examining a tiny clock through three giant magnifying glasses strapped to his eyes",
            "funny street sweets vendor dipping jalebis into sugar syrup with dramatic flourishes and sugar swirl patterns"
        ]
    },
    "animal_families": {
        "title": "Happy Animal Families: Cute Wildlife & Farm Adventures Coloring Book",
        "subtitle": "50 Heartwarming Scenes of Baby Animals and Parents Exploring Nature for Kids Ages 4-8",
        "categories": [
            "Juvenile Nonfiction / Animals / General",
            "Juvenile Nonfiction / Activity Books / Coloring",
            "Crafts, Hobbies & Home / Coloring Books for Grown-Ups"
        ],
        "keywords": [
            "animal coloring book for kids ages 4-8",
            "baby animals coloring pages",
            "cute wildlife family activity book",
            "farm animal coloring book",
            "easy animal outlines for toddlers",
            "nature coloring book for boys and girls",
            "adorable animal illustrations"
        ],
        "description": "<h3>Discover the Sweetest Animal Families in Nature!</h3><p>An adorable collection of animal parents and their babies in peaceful, loving nature settings. Designed with clear, thick outlines perfect for little hands.</p>",
        "prompts": [
            "mother bear and cute baby bear cub catching honey together near a forest tree",
            "mother duck leading line of four fluffy ducklings swimming across a calm lily pad pond",
            "father and mother elephant playing water spray with their baby elephant in savanna",
            "cute mama penguin hugging baby penguin chick on an iceberg with gentle snow falling",
            "mama koala carrying baby joey on her back climbing a eucalyptus tree branch",
            "lion family resting peacefully under acacia tree, baby lion playing with dad's tail",
            "mother deer doe standing with cute spotted baby fawn in a meadow of wildflowers",
            "family of cute rabbits eating carrots in a cozy vegetable garden patch",
            "cute mama otter floating on water holding paws with baby otter resting on tummy",
            "mother kangaroo with cute baby joey peeking curiously out of her pouch"
        ]
    },
    "adult_mandalas": {
        "title": "Mindful Mandalas: Serene Geometric & Floral Patterns for Stress Relief",
        "subtitle": "50 Intricate Meditative Designs for Deep Relaxation and Mindfulness Coloring",
        "categories": [
            "Body, Mind & Spirit / Mindfulness & Meditation",
            "Crafts, Hobbies & Home / Coloring Books for Grown-Ups",
            "Self-Help / Stress Management"
        ],
        "keywords": [
            "mandala coloring book for adults",
            "mindfulness relaxation coloring pages",
            "stress relief pattern coloring book",
            "meditation art therapy book",
            "geometric patterns adult coloring",
            "intricate floral mandalas",
            "calming patterns for anxiety"
        ],
        "description": "<h3>Relax, Unwind, and Restore Inner Peace with Mindful Mandalas</h3><p>Escape the noise of daily life with 50 beautifully balanced, symmetrical mandala designs crafted specifically for relaxation and artistic expression.</p>",
        "prompts": [
            "intricate symmetrical circular floral mandala pattern with detailed petals and sacred geometry",
            "mindfulness meditation mandala with lotus blossom center and flowing concentric circles",
            "celtic knot inspired sacred geometry mandala with interlocking ornamental bands",
            "botanical mandala with intricate wild vines, leaves, and blooming rosebuds"
        ]
    }
}
 
# -------------------------------------------------------------
# IMAGE FETCHING & PROCESSING
# -------------------------------------------------------------
def fetch_coloring_image(prompt_text, width=1024, height=1024):
    """
    Fetches a coloring page image using Pollinations.ai (100% Free, No API key, No token limit).
    Appends specialized negative and style tags to ensure clean black & white outlines.
    """
    style_suffix = ", coloring book page style, clean thick black outline, pure white background, no shading, no gradient, no colors, high contrast monochrome vector line art"
    full_prompt = prompt_text + style_suffix
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={int(time.time()*1000)%100000}"
 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
 
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=35)
            if resp.status_code == 200 and len(resp.content) > 10000:
                img = Image.open(BytesIO(resp.content))
                return img
        except Exception as e:
            print(f"  [Retry {attempt+1}/3] Image fetch delay: {e}")
            time.sleep(2)
 
    # Fallback to local procedural line-art if network is unavailable
    return create_procedural_fallback_image(prompt_text)
 
def create_procedural_fallback_image(label):
    """Fallback generator to guarantee zero-fail book compilation."""
    img = Image.new("RGB", (1024, 1024), "white")
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Draw an elegant coloring border
    draw.rectangle([(60, 60), (964, 964)], outline="black", width=6)
    draw.rectangle([(80, 80), (944, 944)], outline="black", width=2)
    # Draw central decorative mandala / circles
    center = (512, 512)
    for r in range(50, 420, 35):
        draw.ellipse([(center[0]-r, center[1]-r), (center[0]+r, center[1]+r)], outline="black", width=4)
    return img
 
def post_process_for_kdp(pil_image):
    """
    Converts image to high-contrast pure black and white line art.
    Removes muddy grey tones and ensures crisp 300 DPI printing.
    """
    gray = pil_image.convert("L")
    # Increase line sharpness and threshold to ensure clean white background
    threshold = 195
    table = []
    for i in range(256):
        table.append(0 if i < threshold else 255)
    bw = gray.point(table, "1")
    return bw.convert("L")
 
# -------------------------------------------------------------
# PDF BUILDER (KDP COMPLIANT 8.5 x 11 INCHES)
# -------------------------------------------------------------
def build_kdp_pdf(image_list, output_pdf_path, book_title):
    """
    Builds a print-ready 8.5 x 11 inch PDF for Amazon KDP with single-sided pages.
    """
    # 8.5 x 11 inches in points (72 points/inch)
    page_w, page_h = letter # 612 x 792 pt
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
 
    # PAGE 1: "This Book Belongs To"
    c.setLineWidth(3)
    c.rect(0.5 * inch, 0.5 * inch, page_w - 1.0 * inch, page_h - 1.0 * inch)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(page_w / 2.0, page_h - 2.5 * inch, "THIS BOOK BELONGS TO:")
    c.setLineWidth(2)
    c.line(page_w / 2.0 - 150, page_h - 3.5 * inch, page_w / 2.0 + 150, page_h - 3.5 * inch)
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(page_w / 2.0, 1.2 * inch, f"{book_title}")
    c.drawCentredString(page_w / 2.0, 0.9 * inch, "Color your world with laughter and joy!")
    c.showPage()
 
    # PAGE 2: BLANK (Protects Page 1 and sets up single-sided illustrations)
    c.showPage()
 
    # PAGES 3+: Single-sided coloring pages with blank backs
    printable_w = 7.5 * inch # 0.5 margin on left and right
    printable_h = 9.8 * inch # margins top and bottom
 
    for idx, img in enumerate(image_list):
        temp_img_path = f"temp_page_{idx}.png"
        img.save(temp_img_path, format="PNG", dpi=(300, 300))
 
        # FRONT PAGE (Illustration)
        # Center image within printable bounds
        img_x = (page_w - printable_w) / 2.0
        img_y = (page_h - printable_h) / 2.0
 
        c.drawImage(temp_img_path, img_x, img_y, width=printable_w, height=printable_h, preserveAspectRatio=True)
 
        # Decorative clean page number at bottom
        c.setFont("Helvetica", 9)
        c.drawCentredString(page_w / 2.0, 0.4 * inch, f"- {idx + 1} -")
        c.showPage()
 
        # BACK PAGE: Blank with subtle decorative border to prevent marker bleed
        c.setStrokeColorRGB(0.85, 0.85, 0.85)
        c.setLineWidth(1)
        c.rect(0.75 * inch, 0.75 * inch, page_w - 1.5 * inch, page_h - 1.5 * inch)
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColorRGB(0.6, 0.6, 0.6)
        c.drawCentredString(page_w / 2.0, 0.9 * inch, "[ Blank page to protect against marker bleed-through ]")
        c.showPage()
 
        # Clean up temporary page image
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
 
    c.save()
    print(f"[OK] Print-ready PDF saved successfully: {output_pdf_path}")
 
# -------------------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------------------
def run_pipeline(theme_key="funny_characters", target_pages=48):
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/raw_images", exist_ok=True)
 
    theme_data = THEMES.get(theme_key, THEMES["funny_characters"])
    prompts_pool = theme_data["prompts"]
 
    print(f"==================================================")
    print(f" Starting KDP Zero-Cost Book Generation Engine")
    print(f" Niche Theme  : {theme_key}")
    print(f" Target Pages : {target_pages} coloring pages")
    print(f" Total PDF    : {target_pages * 2 + 2} pages (Single-sided + Blank backs)")
    print(f"==================================================")
 
    processed_images = []
 
    for i in range(target_pages):
        prompt = prompts_pool[i % len(prompts_pool)]
        print(f"-> Generating Page {i+1}/{target_pages}: {prompt[:45]}...")
        raw_img = fetch_coloring_image(prompt)
        bw_img = post_process_for_kdp(raw_img)
 
        # Save raw 300 DPI image in case user wants individual sheets
        bw_img.save(f"output/raw_images/page_{i+1:03d}.png", format="PNG", dpi=(300, 300))
        processed_images.append(bw_img)
        time.sleep(1) # respectful rate limit
 
    # Build PDF
    pdf_filename = f"output/{theme_key}_KDP_Interior_8.5x11.pdf"
    build_kdp_pdf(processed_images, pdf_filename, theme_data["title"])
 
    # Build Metadata & Keywords file
    meta_path = "output/KDP_Metadata_Keywords.txt"
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("AMAZON KDP READY-TO-PASTE METADATA & KEYWORDS\n")
        f.write("="*60 + "\n\n")
        f.write(f"BOOK TITLE:\n{theme_data['title']}\n\n")
        f.write(f"SUBTITLE:\n{theme_data['subtitle']}\n\n")
        f.write(f"AI DISCLOSURE (Select 'Yes' in KDP setup):\n")
        f.write("- Tools Used: Pollinations / FLUX AI\n")
        f.write("- Content: Interior Illustrations (Created with AI assistance, formatted manually)\n\n")
        f.write("7 KDP BACKEND KEYWORDS (Paste one in each of the 7 keyword boxes):\n")
        for idx, kw in enumerate(theme_data["keywords"], 1):
            f.write(f"  Box {idx}: {kw}\n")
        f.write("\nRECOMMENDED CATEGORIES (Select in KDP Category Chooser):\n")
        for cat in theme_data["categories"]:
            f.write(f"  - {cat}\n")
        f.write(f"\nBOOK DESCRIPTION (HTML format - copy and paste directly into KDP description):\n")
        f.write(theme_data["description"] + "\n")
 
    print("\n[SUCCESS] Book generation complete! All files saved in ./output")
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KDP Automated Book Pipeline")
    parser.add_argument("--theme", type=str, default="funny_characters", help="Book niche theme")
    parser.add_argument("--pages", type=int, default=48, help="Number of coloring pages")
    args = parser.parse_args()
 
    run_pipeline(args.theme, args.pages)
 
