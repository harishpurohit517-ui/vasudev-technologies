from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os
import smtplib
import json
import ssl
from email.message import EmailMessage

app = Flask(__name__)

# =========================================================
# VASUDEV TECHNOLOGIES - PRODUCTS
# =========================================================

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

# =========================================================
# GMAIL SETTINGS
# =========================================================

SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

BUSINESS_EMAIL = "harishpurohit517@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# =========================================================
# PRODUCT IMAGE
# =========================================================

@app.route("/product-image/<path:filename>")
def product_image(filename):
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    product_json = json.dumps(products)

    html = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>VASUDEV TECHNOLOGIES</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f5f7fb;
    color: #111827;
}

header {
    background: #0b1220;
    color: white;
    padding: 18px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.logo {
    font-size: 25px;
    font-weight: bold;
    letter-spacing: 1px;
}

.cart-button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 11px 18px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 15px;
    font-weight: bold;
}

.cart-button:hover {
    background: #1d4ed8;
}

.hero {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    color: white;
    text-align: center;
    padding: 70px 20px;
}

.hero h1 {
    font-size: 45px;
    margin: 0 0 12px;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
}

.search-area {
    text-align: center;
    padding: 25px 20px;
}

.search-box {
    width: 90%;
    max-width: 650px;
    padding: 15px 20px;
    border: 1px solid #d1d5db;
    border-radius: 12px;
    font-size: 16px;
    outline: none;
}

.products {
    max-width: 1250px;
    margin: auto;
    padding: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 25px;
}

.card {
    background: white;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    transition: 0.25s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 35px rgba(0,0,0,0.13);
}

.product-image {
    width: 100%;
    height: 210px;
    object-fit: contain;
    background: #ffffff;
    padding: 15px;
}

.card-content {
    padding: 18px;
}

.category {
    color: #2563eb;
    font-size: 13px;
    font-weight: bold;
}

.card h2 {
    font-size: 20px;
    margin: 8px 0;
}

.description {
    color: #6b7280;
    font-size: 14px;
    min-height: 38px;
}

.price {
    font-size: 23px;
    font-weight: bold;
    margin: 15px 0;
}

.add-button {
    width: 100%;
    border: none;
    background: #111827;
    color: white;
    padding: 13px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
}

.add-button:hover {
    background: #2563eb;
}

/* CART */

.overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.55);
    z-index: 2000;
}

.cart-panel {
    background: white;
    width: 95%;
    max-width: 520px;
    height: 100%;
    position: absolute;
    right: 0;
    top: 0;
    padding: 25px;
    overflow-y: auto;
}

.cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close {
    border: none;
    background: #ef4444;
    color: white;
    border-radius: 8px;
    padding: 8px 12px;
    cursor: pointer;
}

.cart-item {
    border-bottom: 1px solid #e5e7eb;
    padding: 15px 0;
}

.cart-item-name {
    font-weight: bold;
}

.quantity {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
}

.quantity button {
    width: 30px;
    height: 30px;
    border: none;
    border-radius: 6px;
    background: #e5e7eb;
    cursor: pointer;
}

.remove {
    background: #fee2e2 !important;
    color: #dc2626;
}

.total {
    font-size: 22px;
    font-weight: bold;
    margin: 25px 0;
}

.enquire-button {
    width: 100%;
    padding: 15px;
    border: none;
    border-radius: 10px;
    background: #16a34a;
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

.enquire-button:hover {
    background: #15803d;
}

/* FORM */

.modal {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.65);
    z-index: 3000;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.form-box {
    background: white;
    width: 100%;
    max-width: 450px;
    border-radius: 18px;
    padding: 30px;
}

.form-box h2 {
    margin-top: 0;
}

.form-box input {
    width: 100%;
    padding: 14px;
    margin: 8px 0 15px;
    border: 1px solid #d1d5db;
    border-radius: 9px;
    font-size: 16px;
}

.submit-button {
    width: 100%;
    padding: 14px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    cursor: pointer;
}

.cancel-button {
    width: 100%;
    padding: 12px;
    margin-top: 8px;
    background: #e5e7eb;
    border: none;
    border-radius: 9px;
    cursor: pointer;
}

.message {
    margin-top: 15px;
    padding: 12px;
    border-radius: 8px;
    display: none;
}

.success {
    background: #dcfce7;
    color: #166534;
}

.error {
    background: #fee2e2;
    color: #991b1b;
}

footer {
    margin-top: 60px;
    padding: 35px;
    background: #0b1220;
    color: white;
    text-align: center;
}

@media(max-width:600px) {

    .hero h1 {
        font-size: 32px;
    }

    .logo {
        font-size: 19px;
    }

}

</style>

</head>

<body>

<header>

<div class="logo">
VASUDEV TECHNOLOGIES
</div>

<button class="cart-button" onclick="openCart()">
🛒 Cart (<span id="cartCount">0</span>)
</button>

</header>


<section class="hero">

<h1>VASUDEV TECHNOLOGIES</h1>

<p>
Laptop Parts • Computer Accessories • Quality Products
</p>

</section>


<div class="search-area">

<input
class="search-box"
id="search"
placeholder="Search products..."
oninput="searchProducts()"
>

</div>


<div class="products" id="products"></div>


<footer>

<h2>VASUDEV TECHNOLOGIES</h2>

<p>Quality laptop parts and computer accessories.</p>

<p>© 2026 VASUDEV TECHNOLOGIES</p>

</footer>


<!-- CART -->

<div class="overlay" id="cartOverlay">

<div class="cart-panel">

<div class="cart-header">

<h2>🛒 Your Cart</h2>

<button class="close" onclick="closeCart()">
Close
</button>

</div>

<div id="cartItems"></div>

<div class="total">
Total: ₹<span id="cartTotal">0</span>
</div>

<button class="enquire-button" onclick="openEnquiry()">
Enquire About These Products
</button>

</div>

</div>


<!-- ENQUIRY FORM -->

<div class="modal" id="enquiryModal">

<div class="form-box">

<h2>Customer Enquiry</h2>

<p>
Enter your details and we will contact you.
</p>

<label>Name</label>

<input
id="customerName"
type="text"
placeholder="Your name"
>

<label>Phone Number</label>

<input
id="customerPhone"
type="tel"
placeholder="Your phone number"
>

<button
class="submit-button"
onclick="submitEnquiry()"
>
Send Enquiry
</button>

<button
class="cancel-button"
onclick="closeEnquiry()"
>
Cancel
</button>

<div id="message" class="message"></div>

</div>

</div>


<script>

const products = PRODUCT_DATA;

let cart = [];


function displayProducts(list = products) {

    const container = document.getElementById("products");

    container.innerHTML = "";

    if (list.length === 0) {

        container.innerHTML =
            "<p style='text-align:center;grid-column:1/-1;'>No products found.</p>";

        return;
    }

    list.forEach(product => {

        container.innerHTML += `

        <div class="card">

            <img
                class="product-image"
                src="/product-image/${product.image}"
                alt="${product.name}"
                onerror="this.style.display='none'"
            >

            <div class="card-content">

                <div class="category">
                    ${product.category}
                </div>

                <h2>
                    ${product.name}
                </h2>

                <div class="description">
                    ${product.description}
                </div>

                <div class="price">
                    ₹${product.price.toLocaleString("en-IN")}
                </div>

                <button
                    class="add-button"
                    onclick="addToCart(${product.id})"
                >
                    Add to Cart
                </button>

            </div>

        </div>

        `;

    });

}


function addToCart(id) {

    const existing = cart.find(item => item.id === id);

    if (existing) {

        existing.quantity++;

    } else {

        const product = products.find(p => p.id === id);

        cart.push({
            ...product,
            quantity: 1
        });

    }

    updateCart();

}


function increaseQuantity(id) {

    const item = cart.find(p => p.id === id);

    if (item) {
        item.quantity++;
    }

    updateCart();

}


function decreaseQuantity(id) {

    const item = cart.find(p => p.id === id);

    if (!item) return;

    item.quantity--;

    if (item.quantity <= 0) {

        cart = cart.filter(p => p.id !== id);

    }

    updateCart();

}


function removeFromCart(id) {

    cart = cart.filter(p => p.id !== id);

    updateCart();

}


function updateCart() {

    const count = cart.reduce(
        (sum, item) => sum + item.quantity,
        0
    );

    document.getElementById("cartCount").innerText = count;

    const container = document.getElementById("cartItems");

    container.innerHTML = "";

    let total = 0;

    if (cart.length === 0) {

        container.innerHTML =
            "<p>Your cart is empty.</p>";

    }

    cart.forEach(item => {

        const subtotal = item.price * item.quantity;

        total += subtotal;

        container.innerHTML += `

        <div class="cart-item">

            <div class="cart-item-name">
                ${item.name}
            </div>

            <div>
                ₹${item.price.toLocaleString("en-IN")}
                × ${item.quantity}
            </div>

            <div>
                Subtotal:
                ₹${subtotal.toLocaleString("en-IN")}
            </div>

            <div class="quantity">

                <button onclick="decreaseQuantity(${item.id})">
                    −
                </button>

                <span>
                    ${item.quantity}
                </span>

                <button onclick="increaseQuantity(${item.id})">
                    +
                </button>

                <button
                    class="remove"
                    onclick="removeFromCart(${item.id})"
                >
                    Remove
                </button>

            </div>

        </div>

        `;

    });

    document.getElementById("cartTotal").innerText =
        total.toLocaleString("en-IN");

}


function openCart() {

    document.getElementById("cartOverlay").style.display =
        "block";

}


function closeCart() {

    document.getElementById("cartOverlay").style.display =
        "none";

}


function openEnquiry() {

    if (cart.length === 0) {

        alert("Please add at least one product to the cart.");

        return;
    }

    document.getElementById("enquiryModal").style.display =
        "flex";

}


function closeEnquiry() {

    document.getElementById("enquiryModal").style.display =
        "none";

}


function submitEnquiry() {

    const name =
        document.getElementById("customerName").value.trim();

    const phone =
        document.getElementById("customerPhone").value.trim();

    const message =
        document.getElementById("message");


    if (!name) {

        showMessage(
            "Please enter your name.",
            false
        );

        return;
    }


    if (!phone) {

        showMessage(
            "Please enter your phone number.",
            false
        );

        return;
    }


    if (cart.length === 0) {

        showMessage(
            "Your cart is empty.",
            false
        );

        return;
    }


    message.style.display = "block";

    message.className = "message";

    message.innerText =
        "Sending enquiry...";


    fetch("/enquiry", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name,

            phone: phone,

            cart: cart.map(item => ({

                id: item.id,

                quantity: item.quantity

            }))

        })

    })

    .then(response => response.json())

    .then(data => {

        if (data.success) {

            message.className =
                "message success";

            message.innerText =
                "✅ Enquiry sent successfully!";

            cart = [];

            updateCart();

            setTimeout(() => {

                closeEnquiry();

                closeCart();

                document.getElementById("customerName").value = "";

                document.getElementById("customerPhone").value = "";

                message.style.display = "none";

            }, 1800);

        } else {

            showMessage(
                data.error || "Could not send enquiry.",
                false
            );

        }

    })

    .catch(error => {

        console.error(error);

        showMessage(
            "Could not connect to the server.",
            false
        );

    });

}


function showMessage(text, success) {

    const message =
        document.getElementById("message");

    message.style.display = "block";

    message.className =
        success
        ? "message success"
        : "message error";

    message.innerText = text;

}


function searchProducts() {

    const query =
        document.getElementById("search").value
        .toLowerCase()
        .trim();

    const filtered = products.filter(product =>

        product.name.toLowerCase().includes(query) ||

        product.category.toLowerCase().includes(query) ||

        product.description.toLowerCase().includes(query)

    );

    displayProducts(filtered);

}


displayProducts();

updateCart();

</script>

</body>

</html>
"""

    html = html.replace(
        "PRODUCT_DATA",
        product_json
    )

    return render_template_string(html)


# =========================================================
# ENQUIRY
# =========================================================

@app.route("/enquiry", methods=["POST"])
def enquiry():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request."
            }), 400


        name = str(data.get("name", "")).strip()

        phone = str(data.get("phone", "")).strip()

        cart = data.get("cart", [])


        if not name:

            return jsonify({
                "success": False,
                "error": "Please enter your name."
            }), 400


        if not phone:

            return jsonify({
                "success": False,
                "error": "Please enter your phone number."
            }), 400


        if not isinstance(cart, list) or len(cart) == 0:

            return jsonify({
                "success": False,
                "error": "Cart is empty."
            }), 400


        # -------------------------------------------------
        # BUILD EMAIL
        # -------------------------------------------------

        email_lines = []

        email_lines.append(
            "=================================================="
        )

        email_lines.append(
            "NEW CUSTOMER ENQUIRY"
        )

        email_lines.append(
            "=================================================="
        )

        email_lines.append("")

        email_lines.append(
            "VASUDEV TECHNOLOGIES"
        )

        email_lines.append("")

        email_lines.append(
            "CUSTOMER DETAILS"
        )

        email_lines.append(
            "----------------"
        )

        email_lines.append(
            f"Customer Name: {name}"
        )

        email_lines.append(
            f"Phone Number: {phone}"
        )

        email_lines.append("")

        email_lines.append(
            "PRODUCTS ENQUIRED"
        )

        email_lines.append(
            "-----------------"
        )

        total = 0

        valid_product_found = False


        for cart_item in cart:

            try:

                product_id = int(
                    cart_item.get("id")
                )

                quantity = int(
                    cart_item.get("quantity", 1)
                )

            except:

                continue


            if quantity <= 0:
                continue


            product = next(
                (
                    p for p in products
                    if p["id"] == product_id
                ),
                None
            )


            if product is None:
                continue


            valid_product_found = True

            subtotal = (
                product["price"] * quantity
            )

            total += subtotal


            email_lines.append("")

            email_lines.append(
                product["name"]
            )

            email_lines.append(
                f"Category: {product['category']}"
            )

            email_lines.append(
                f"Quantity: {quantity}"
            )

            email_lines.append(
                f"Price: ₹{product['price']:,}"
            )

            email_lines.append(
                f"Subtotal: ₹{subtotal:,}"
            )


        if not valid_product_found:

            return jsonify({
                "success": False,
                "error": "No valid products found."
            }), 400


        email_lines.append("")

        email_lines.append(
            "--------------------------------------------------"
        )

        email_lines.append(
            f"TOTAL: ₹{total:,}"
        )

        email_lines.append(
            "--------------------------------------------------"
        )

        email_lines.append("")

        email_lines.append(
            "This enquiry was submitted through"
        )

        email_lines.append(
            "the VASUDEV TECHNOLOGIES website."
        )

        email_lines.append("")


        email_body = "\n".join(email_lines)


        # -------------------------------------------------
        # CHECK ENVIRONMENT VARIABLES
        # -------------------------------------------------

        if not SMTP_EMAIL or not SMTP_PASSWORD:

            print("")
            print("==================================================")
            print("GMAIL SETTINGS ARE NOT CONFIGURED")
            print("==================================================")
            print(email_body)
            print("==================================================")

            return jsonify({
                "success": False,
                "error": "Email system is not configured yet."
            }), 500


        # -------------------------------------------------
        # CREATE EMAIL
        # -------------------------------------------------

        msg = EmailMessage()

        msg["Subject"] = (
            f"New VASUDEV Enquiry - {name}"
        )

        msg["From"] = SMTP_EMAIL

        msg["To"] = BUSINESS_EMAIL

        msg.set_content(email_body)


        # -------------------------------------------------
        # CONNECT TO GMAIL SMTP
        # -------------------------------------------------

        print("")
        print("Connecting to Gmail SMTP...")

        context = ssl.create_default_context()


        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=30
        ) as server:

            server.ehlo()

            server.starttls(
                context=context
            )

            server.ehlo()

            server.login(
                SMTP_EMAIL,
                SMTP_PASSWORD
            )

            server.send_message(msg)


        print("")
        print("==================================================")
        print("EMAIL SENT SUCCESSFULLY")
        print("==================================================")
        print(email_body)
        print("==================================================")


        return jsonify({
            "success": True,
            "message": "Enquiry sent successfully."
        })


    except smtplib.SMTPAuthenticationError:

        print("")
        print("GMAIL AUTHENTICATION ERROR")
        print("Check SMTP_EMAIL and SMTP_PASSWORD.")
        print("")


        return jsonify({
            "success": False,
            "error": "Gmail authentication failed. Check the Gmail App Password in Render."
        }), 500


    except smtplib.SMTPConnectError:

        print("")
        print("GMAIL CONNECTION ERROR")
        print("Could not connect to Gmail SMTP.")
        print("")


        return jsonify({
            "success": False,
            "error": "Could not connect to Gmail SMTP server."
        }), 500


    except smtplib.SMTPException as e:

        print("")
        print("SMTP ERROR:")
        print(str(e))
        print("")


        return jsonify({
            "success": False,
            "error": "Gmail SMTP error occurred."
        }), 500


    except Exception as e:

        print("")
        print("GENERAL EMAIL ERROR:")
        print(str(e))
        print("")


        return jsonify({
            "success": False,
            "error": "Could not send enquiry email."
        }), 500


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get("PORT", 5000)
        ),
        debug=False
    )