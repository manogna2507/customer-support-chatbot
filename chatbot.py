import json
import random
import pickle
import re
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

from db import get_all_products

lemmatizer = WordNetLemmatizer()

# Load trained model
model = load_model("models/chatbot_model.keras")

# Load vocabulary and classes
words = pickle.load(open("models/words.pkl", "rb"))
classes = pickle.load(open("models/classes.pkl", "rb"))

# Load intents
with open("data/intents.json", "r") as file:
    intents = json.load(file)

# Load products
products = get_all_products()

# Temporary orders list
# Replace this later with your actual orders database/file
orders = []


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [
        lemmatizer.lemmatize(word.lower())
        for word in sentence_words
    ]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)

    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)

    prediction = model.predict(
        np.array([bow]),
        verbose=0
    )[0]

    ERROR_THRESHOLD = 0.60

    results = [
        (i, r)
        for i, r in enumerate(prediction)
        if r > ERROR_THRESHOLD
    ]

    results.sort(key=lambda x: x[1], reverse=True)

    intents_list = []

    for r in results:
        intents_list.append(
            {
                "intent": classes[r[0]],
                "probability": str(r[1])
            }
        )

    return intents_list


def search_product(message):
    message = message.lower()

    stop_words = {
        "i", "need", "want", "show", "me",
        "a", "an", "the", "please",
        "looking", "for"
    }

    keywords = [
        word for word in message.split()
        if word not in stop_words
    ]

    matches = []

    for product in products:
        searchable_text = (
            product["name"] + " " +
            product["category"] + " " +
            product["description"]
        ).lower()

        if any(keyword in searchable_text for keyword in keywords):
            matches.append(product)

    if not matches:
        return None

    response = "🛍 Here are some products I found:\n\n"

    for product in matches[:3]:
        response += (
            f"📦 {product['name']}\n"
            f"💰 ₹{product['price']}\n"
            f"⭐ {product['rating']}/5\n"
            f"📂 {product['category']}\n\n"
        )

    return response


def search_order(message):
    message = message.upper()

    match = re.search(r"ORD\d+", message)

    if not match:
        return None

    order_id = match.group()

    for order in orders:
        if order["order_id"] == order_id:
            return (
                f"📦 Order Details\n\n"
                f"🆔 Order ID: {order['order_id']}\n"
                f"🛍 Product: {order['product']}\n"
                f"📍 Status: {order['status']}\n"
                f"🚚 Expected Delivery: {order['expected_delivery']}"
            )

    return "❌ Sorry, I couldn't find that order ID."


def get_response(message, intents_list):

    order = search_order(message)
    if order:
        return order

    product = search_product(message)
    if product:
        return product

    if not intents_list:
        return (
            "Sorry, I couldn't understand your question.\n\n"
            "You can ask me about:\n"
            "📦 Orders\n"
            "🔄 Refunds\n"
            "💳 Payments\n"
            "🛍 Products"
        )

    tag = intents_list[0]["intent"]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, I couldn't understand your question."


if __name__ == "__main__":

    print("🤖 ShopSmart AI Chatbot")
    print("Type 'quit' to exit.\n")

    while True:

        message = input("You: ")

        if message.lower() == "quit":
            break

        intents_list = predict_class(message)

        response = get_response(message, intents_list)

        print("Bot:", response)