#include <Arduino.h>
// File will exist once project is built
#include "genned_json/test_json.hpp"

void setup() {
    Serial.begin(115200);
}

void loop() {
    // Get compiled JSON document
    const json2cpp::json& theJsonDoc = compiled_json::test_json::get();
    // We know this is an array, so let's iterate through it
    Serial.println("JSON doc size: " + String(theJsonDoc.size()));
    Serial.println("Elements in array:");
    for(const auto& elem : theJsonDoc) {
        Serial.println(elem.get<double>());
    }
    delay(1000);
}