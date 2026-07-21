import json
import random
import pickle
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

lemmatizer = WordNetLemmatizer()

# Load intents
with open("data/intents.json") as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]

# Read patterns
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        documents.append((tokens, intent["tag"]))

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatize
words = sorted(set(
    lemmatizer.lemmatize(word.lower())
    for word in words
    if word not in ignore_letters
))

classes = sorted(set(classes))

# Save vocabulary
pickle.dump(words, open("models/words.pkl", "wb"))
pickle.dump(classes, open("models/classes.pkl", "wb"))

training = []

output_empty = [0] * len(classes)

# Create Bag of Words
for document in documents:

    bag = []

    pattern_words = [
        lemmatizer.lemmatize(word.lower())
        for word in document[0]
    ]

    for word in words:
        bag.append(1 if word in pattern_words else 0)

    output_row = output_empty[:]
    output_row[classes.index(document[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)

train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])

# Build Neural Network
model = Sequential()

model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))

model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))

model.add(Dense(len(train_y[0]), activation="softmax"))

model.compile(
    loss="categorical_crossentropy",
    optimizer=Adam(learning_rate=0.001),
    metrics=["accuracy"]
)

print("Training model...")

model.fit(
    train_x,
    train_y,
    epochs=200,
    batch_size=5,
    verbose=1
)

model.save("models/chatbot_model.keras")

print("\nTraining Complete!")