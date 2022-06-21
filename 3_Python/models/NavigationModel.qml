import QtQuick 2.0


ListModel {
    ListElement {
        logo: "./res/topics_icon.svg"
        name: "Темы"
        to_navigate: "topics.qml"
    }
    ListElement {
        logo: "./res/tests_icon.svg"
        name: "Тесты"
        to_navigate: "tests.qml"
    }
    ListElement {
        logo: "./res/generator_icon.svg"
        name: "Генератор примеров"
        to_navigate: "generator.qml"
    }
    ListElement {
        logo: "./res/profile_icon.svg"
        name: "Профиль"
        to_navigate: "profile.qml"
    }
}