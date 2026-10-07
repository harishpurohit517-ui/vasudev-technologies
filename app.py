from flask import Flask, request, jsonify, send_from_directory
from email.message import EmailMessage
import smtplib
import os
import json

app = Flask(__name__)

# ============================================================
# VASUDEV TECHNOLOGIES
# ============================================================

products = [
    {
        "id": 1,
        "name": "1.8 GB RAM",
        "price": 3000,
        "category": "RAM",
        "description": "1.8 GB laptop RAM",
        "image": "ram.jfif"
    },
    {
        "id": 2,
        "name": "Dell Keyboard + Mouse Combo",
        "price": 1000,
        "category": "Keyboard & Mouse",
        "description": "Dell keyboard and mouse combo",
        "image": "dell_combo.jfif"
    },
    {
        "id": 3,
        "name": "HS04 Battery",
        "price": 700,
        "category": "Battery",
        "description": "HS04 laptop battery",
        "image": "hs04_battery.jfif"
    },
    {
        "id": 4,
        "name": "256 GB SSD",
        "price": 2000,
        "category": "SSD",
        "description": "256 GB laptop SSD",
        "image": "ssd_256gb.jfif"
    },
    {
        "id": 5,
        "name": "Laptop Screen",
        "price": 5000,
        "category": "Screen",
        "description": "Laptop replacement screen",
        "image": "laptop_screen.jfif"
    },
    {
        "id": 6,
        "name": "Laptop Panel",
        "price": 700,
        "category": "Panel",
        "description": "Laptop replacement panel",
        "image": "laptop_panel.jfif"
    },
    {
        "id": 7,
        "name": "Laptop Touchpad",
        "price": 700,
        "category": "Touchpad",
        "description": "Laptop replacement touchpad",
        "image": "laptop_touchpad.jfif"
    }
]

# ============================================================
# EMAIL SETTINGS
# ============================================================

SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

BUSINESS_EMAIL = "harishpurohit517@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ============================================================
# PRODUCT IMAGE ROUTE
# ============================================================

@app.route("/product-image/<filename>")
def product_image(filename):
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    product_json = json.dumps(products)

    product_html = ""

    for product in products:

        product_html += f"""
        <div class="product-card"
             data-name="{product['name'].lower()}"
             data-category="{product['category'].lower()}">

            <div class="image-box">
                <img src="/product-image/{product['image']}"
                     alt="{product['name']}">
            </div>

            <div class="product-info">

                <div class="category">
                    {product['category']}
                </div>

                <h2>{product['name']}</h2>

                <p>{product['description']}</p>

                <div class="price">
                    ₹{product['price']:,}
                </div>

                <button
                    class="add-button"
                    onclick="addToCart({product['id']})">

                    Add to Cart

                </button>

            </div>

        </div>
        """

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>VASUDEV TECHNOLOGIES</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    color: #111827;
}}

/* HEADER */

header {{
    background: #111827;
    color: white;

    padding: 18px 30px;

    display: flex;
    justify-content: space-between;
    align-items: center;

    position: sticky;
    top: 0;

    z-index: 100;
}}

.logo {{
    font-size: 24px;
    font-weight: bold;
}}

.cart-button {{
    background: white;
    color: #111827;

    border: none;
    border-radius: 10px;

    padding: 11px 18px;

    font-weight: bold;
    cursor: pointer;
}}

.cart-button:hover {{
    background: #e5e7eb;
}}

/* HERO */

.hero {{
    background: linear-gradient(
        135deg,
        #111827,
        #374151
    );

    color: white;

    padding: 65px 20px;

    text-align: center;
}}

.hero h1 {{
    font-size: 42px;
    margin: 0 0 10px;
}}

.hero p {{
    font-size: 18px;
    opacity: 0.9;
}}

.search-container {{
    max-width: 700px;
    margin: 30px auto 0;
}}

.search {{
    width: 100%;

    padding: 15px 18px;

    border: none;
    border-radius: 12px;

    font-size: 16px;

    outline: none;
}}

/* PRODUCTS */

.products {{
    max-width: 1200px;

    margin: 40px auto;

    padding: 0 20px;

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(250px, 1fr));

    gap: 25px;
}}

.product-card {{
    background: white;

    border-radius: 16px;

    overflow: hidden;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.08);

    transition: 0.2s;
}}

.product-card:hover {{
    transform: translateY(-5px);
}}

.image-box {{
    height: 220px;

    background: #f9fafb;

    display: flex;

    justify-content: center;
    align-items: center;

    padding: 15px;
}}

.image-box img {{
    max-width: 100%;
    max-height: 190px;

    object-fit: contain;
}}

.product-info {{
    padding: 20px;
}}

.category {{
    font-size: 13px;

    color: #6b7280;

    font-weight: bold;

    text-transform: uppercase;
}}

.product-info h2 {{
    font-size: 21px;

    margin: 8px 0;
}}

.product-info p {{
    color: #6b7280;

    min-height: 40px;
}}

.price {{
    font-size: 22px;

    font-weight: bold;

    margin: 15px 0;
}}

.add-button {{
    width: 100%;

    padding: 13px;

    background: #111827;

    color: white;

    border: none;

    border-radius: 9px;

    font-size: 15px;

    font-weight: bold;

    cursor: pointer;
}}

.add-button:hover {{
    background: #374151;
}}

/* CART OVERLAY */

.cart-overlay {{
    display: none;

    position: fixed;

    inset: 0;

    background: rgba(0,0,0,0.55);

    z-index: 500;
}}

.cart-panel {{
    position: absolute;

    right: 0;
    top: 0;

    width: min(450px, 100%);

    height: 100%;

    background: white;

    padding: 25px;

    overflow-y: auto;
}}

.cart-header {{
    display: flex;

    justify-content: space-between;

    align-items: center;
}}

.close {{
    border: none;

    background: #eeeeee;

    width: 36px;
    height: 36px;

    border-radius: 50%;

    font-size: 22px;

    cursor: pointer;
}}

.cart-item {{
    padding: 16px 0;

    border-bottom: 1px solid #ddd;
}}

.cart-item-top {{
    display: flex;

    justify-content: space-between;

    gap: 10px;
}}

.cart-item-name {{
    font-weight: bold;
}}

.remove {{
    border: none;

    background: #fee2e2;

    color: #b91c1c;

    padding: 6px 9px;

    border-radius: 6px;

    cursor: pointer;
}}

.quantity {{
    display: flex;

    align-items: center;

    gap: 10px;

    margin-top: 10px;
}}

.quantity button {{
    width: 30px;
    height: 30px;

    border: none;

    border-radius: 6px;

    background: #e5e7eb;

    cursor: pointer;

    font-size: 18px;
}}

.cart-total {{
    font-size: 23px;

    font-weight: bold;

    margin-top: 20px;
}}

.enquire-button {{
    width: 100%;

    margin-top: 15px;

    padding: 14px;

    border: none;

    border-radius: 10px;

    background: #16a34a;

    color: white;

    font-size: 16px;

    font-weight: bold;

    cursor: pointer;
}}

/* MODAL */

.modal {{
    display: none;

    position: fixed;

    inset: 0;

    background: rgba(0,0,0,0.65);

    z-index: 1000;

    align-items: center;

    justify-content: center;

    padding: 20px;
}}

.modal-box {{
    background: white;

    width: min(450px, 100%);

    border-radius: 16px;

    padding: 25px;
}}

.modal-box h2 {{
    margin-top: 0;
}}

.modal-box input {{
    width: 100%;

    padding: 13px;

    margin: 8px 0 15px;

    border: 1px solid #d1d5db;

    border-radius: 8px;

    font-size: 16px;
}}

.submit-button {{
    width: 100%;

    padding: 14px;

    border: none;

    border-radius: 9px;

    background: #111827;

    color: white;

    font-weight: bold;

    cursor: pointer;
}}

.cancel-button {{
    width: 100%;

    padding: 12px;

    margin-top: 8px;

    border: none;

    border-radius: 9px;

    background: #e5e7eb;

    cursor: pointer;
}}

.message {{
    margin-top: 15px;

    padding: 12px;

    border-radius: 8px;

    display: none;
}}

.success {{
    background: #dcfce7;
    color: #166534;
}}

.error {{
    background: #fee2e2;
    color: #991b1b;
}}

/* FOOTER */

footer {{
    background: #111827;

    color: white;

    text-align: center;

    padding: 25px;

    margin-top: 50px;
}}

/* MOBILE */

@media (max-width: 600px) {{

    header {{
        padding: 15px;
    }}

    .logo {{
        font-size: 18px;
    }}

    .cart-button {{
        padding: 9px 12px;
    }}

    .hero h1 {{
        font-size: 30px;
    }}

}}

</style>

</head>

<body>

<!-- HEADER -->

<header>

    <div class="logo">
        VASUDEV TECHNOLOGIES
    </div>

    <button
        class="cart-button"
        onclick="openCart()">

        🛒 Cart
        <span id="cartCount">0</span>

    </button>

</header>


<!-- HERO -->

<section class="hero">

    <h1>VASUDEV TECHNOLOGIES</h1>

    <p>
        Laptop Parts & Computer Accessories
    </p>

    <div class="search-container">

        <input
            id="search"
            class="search"
            type="text"
            placeholder="Search products..."
            oninput="searchProducts()">

    </div>

</section>


<!-- PRODUCTS -->

<section
    class="products"
    id="products">

    {product_html}

</section>


<!-- FOOTER -->

<footer>

    © 2026 VASUDEV TECHNOLOGIES

</footer>


<!-- CART -->

<div
    class="cart-overlay"
    id="cartOverlay">

    <div class="cart-panel">

        <div class="cart-header">

            <h2>🛒 Your Cart</h2>

            <button
                class="close"
                onclick="closeCart()">

                ×

            </button>

        </div>

        <div id="cartItems"></div>

        <div
            class="cart-total"
            id="cartTotal">

            Total: ₹0

        </div>

        <button
            class="enquire-button"
            onclick="openEnquiry()">

            Enquire Now

        </button>

    </div>

</div>


<!-- ENQUIRY MODAL -->

<div
    class="modal"
    id="enquiryModal">

    <div class="modal-box">

        <h2>Customer Details</h2>

        <p>
            Enter your details and we will contact you.
        </p>

        <input
            id="customerName"
            type="text"
            placeholder="Your Name">

        <input
            id="customerPhone"
            type="tel"
            placeholder="Phone Number">

        <button
            class="submit-button"
            onclick="submitEnquiry()">

            Send Enquiry

        </button>

        <button
            class="cancel-button"
            onclick="closeEnquiry()">

            Cancel

        </button>

        <div
            id="message"
            class="message">

        </div>

    </div>

</div>


<script>

const products = {product_json};

let cart = [];


function addToCart(id) {{

    const product = products.find(
        p => p.id === id
    );

    if (!product) return;


    const existing = cart.find(
        item => item.id === id
    );


    if (existing) {{

        existing.quantity++;

    }} else {{

        cart.push({{
            ...product,
            quantity: 1
        }});

    }}


    updateCart();

    alert(
        product.name +
        " added to cart!"
    );

}}


function updateCart() {{

    const cartItems =
        document.getElementById("cartItems");

    const cartCount =
        document.getElementById("cartCount");

    const cartTotal =
        document.getElementById("cartTotal");


    let total = 0;

    let count = 0;


    if (cart.length === 0) {{

        cartItems.innerHTML =
            '<div class="empty">Your cart is empty.</div>';

    }} else {{

        cartItems.innerHTML =
            cart.map(item => {{

                const itemTotal =
                    item.price *
                    item.quantity;

                total += itemTotal;

                count += item.quantity;


                return `
                    <div class="cart-item">

                        <div class="cart-item-top">

                            <div class="cart-item-name">
                                ${{item.name}}
                            </div>

                            <button
                                class="remove"
                                onclick="removeFromCart(${{item.id}})">

                                Remove

                            </button>

                        </div>

                        <div>
                            ₹${{item.price.toLocaleString()}}
                        </div>

                        <div class="quantity">

                            <button
                                onclick="changeQuantity(
                                    ${{item.id}}, -1
                                )">

                                −

                            </button>

                            <strong>
                                ${{item.quantity}}
                            </strong>

                            <button
                                onclick="changeQuantity(
                                    ${{item.id}}, 1
                                )">

                                +

                            </button>

                            <span>
                                ₹${{
                                    itemTotal.toLocaleString()
                                }}
                            </span>

                        </div>

                    </div>
                `;

            }}).join("");

    }}


    cartCount.textContent = count;

    cartTotal.textContent =
        "Total: ₹" +
        total.toLocaleString();

}}


function changeQuantity(id, change) {{

    const item = cart.find(
        item => item.id === id
    );

    if (!item) return;


    item.quantity += change;


    if (item.quantity <= 0) {{

        cart = cart.filter(
            item => item.id !== id
        );

    }}


    updateCart();

}}


function removeFromCart(id) {{

    cart = cart.filter(
        item => item.id !== id
    );

    updateCart();

}}


function openCart() {{

    document.getElementById(
        "cartOverlay"
    ).style.display = "block";

}}


function closeCart() {{

    document.getElementById(
        "cartOverlay"
    ).style.display = "none";

}}


function openEnquiry() {{

    if (cart.length === 0) {{

        alert(
            "Please add at least one product."
        );

        return;

    }}


    document.getElementById(
        "enquiryModal"
    ).style.display = "flex";

}}


function closeEnquiry() {{

    document.getElementById(
        "enquiryModal"
    ).style.display = "none";

}}


async function submitEnquiry() {{

    const name =
        document.getElementById(
            "customerName"
        ).value.trim();


    const phone =
        document.getElementById(
            "customerPhone"
        ).value.trim();


    const message =
        document.getElementById(
            "message"
        );


    if (!name) {{

        showMessage(
            "Please enter your name.",
            false
        );

        return;

    }}


    if (!phone) {{

        showMessage(
            "Please enter your phone number.",
            false
        );

        return;

    }}


    try {{

        const response =
            await fetch(
                "/enquiry",
                {{
                    method: "POST",

                    headers: {{
                        "Content-Type":
                            "application/json"
                    }},

                    body: JSON.stringify({{
                        name: name,
                        phone: phone,
                        cart: cart
                    }})
                }}
            );


        const data =
            await response.json();


        if (data.success) {{

            showMessage(
                "Enquiry sent successfully! We will contact you soon.",
                true
            );


            cart = [];

            updateCart();


            document.getElementById(
                "customerName"
            ).value = "";


            document.getElementById(
                "customerPhone"
            ).value = "";

        }} else {{

            showMessage(
                data.message ||
                "Unable to send enquiry.",
                false
            );

        }}

    }} catch (error) {{

        showMessage(
            "Could not connect to the server.",
            false
        );

    }}

}}


function showMessage(text, success) {{

    const message =
        document.getElementById(
            "message"
        );


    message.textContent = text;


    message.className =
        "message " +
        (success ? "success" : "error");


    message.style.display = "block";

}}


function searchProducts() {{

    const query =
        document.getElementById(
            "search"
        ).value
        .toLowerCase()
        .trim();


    document
        .querySelectorAll(".product-card")
        .forEach(card => {{

            const name =
                card.dataset.name;

            const category =
                card.dataset.category;


            if (
                name.includes(query) ||
                category.includes(query)
            ) {{

                card.style.display = "block";

            }} else {{

                card.style.display = "none";

            }}

        }});

}}


updateCart();

</script>

</body>

</html>
"""

    return html


# ============================================================
# ENQUIRY API
# ============================================================

@app.route("/enquiry", methods=["POST"])
def enquiry():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400


        name = str(
            data.get("name", "")
        ).strip()


        phone = str(
            data.get("phone", "")
        ).strip()


        cart = data.get("cart", [])


        if not name:

            return jsonify({
                "success": False,
                "message": "Name is required."
            }), 400


        if not phone:

            return jsonify({
                "success": False,
                "message": "Phone number is required."
            }), 400


        if not cart:

            return jsonify({
                "success": False,
                "message": "Cart is empty."
            }), 400


        # ====================================================
        # BUILD EMAIL
        # ====================================================

        total = 0

        product_lines = []


        for item in cart:

            product_name = str(
                item.get(
                    "name",
                    "Unknown Product"
                )
            )


            price = float(
                item.get("price", 0)
            )


            quantity = int(
                item.get("quantity", 1)
            )


            item_total = (
                price * quantity
            )


            total += item_total


            product_lines.append(
                f"{product_name}\n"
                f"Quantity: {quantity}\n"
                f"Price: ₹{price:,.0f}\n"
                f"Subtotal: ₹{item_total:,.0f}\n"
            )


        email_body = f"""
NEW CUSTOMER ENQUIRY
====================

VASUDEV TECHNOLOGIES

Customer Name:
{name}

Phone Number:
{phone}

PRODUCTS ENQUIRED
-----------------

{chr(10).join(product_lines)}

-----------------

TOTAL:
₹{total:,.0f}

-----------------

This enquiry was submitted through
the VASUDEV TECHNOLOGIES website.
"""


        # ====================================================
        # CHECK GMAIL SETTINGS
        # ====================================================

        if not SMTP_EMAIL or not SMTP_PASSWORD:

            print("\n")
            print("=" * 50)
            print("GMAIL SETTINGS ARE NOT CONFIGURED")
            print("=" * 50)
            print(email_body)
            print("=" * 50)


            return jsonify({
                "success": False,
                "message":
                    "Email system is not configured yet."
            }), 500


        # ====================================================
        # CREATE EMAIL
        # ====================================================

        email = EmailMessage()


        email["Subject"] = (
            f"New Enquiry - {name} - "
            f"VASUDEV TECHNOLOGIES"
        )


        email["From"] = SMTP_EMAIL

        email["To"] = BUSINESS_EMAIL


        email.set_content(email_body)


        # ====================================================
        # SEND EMAIL
        # ====================================================

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                SMTP_EMAIL,
                SMTP_PASSWORD
            )

            server.send_message(email)


        print("\n")
        print("=" * 50)
        print("EMAIL SENT SUCCESSFULLY")
        print("=" * 50)
        print(email_body)
        print("=" * 50)


        return jsonify({
            "success": True,
            "message":
                "Enquiry sent successfully."
        })


    except Exception as e:

        print("\n")
        print("=" * 50)
        print("EMAIL ERROR")
        print("=" * 50)
        print(str(e))
        print("=" * 50)


        return jsonify({
            "success": False,
            "message":
                "Unable to send enquiry right now."
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )