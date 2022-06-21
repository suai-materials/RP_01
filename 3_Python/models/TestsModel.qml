import QtQuick 2.0

ListModel {
    ListElement {
        type: "topic"
        name: "Тема 1"
        grade: 5
    }
    ListElement {
        type: "topicTestRunnable"
        name: "Тест 1"
    }
    ListElement {
        type: "topicTest"
        name: "Тест 2"
        grade: 5
    }
    ListElement {
        type: "subTopic"
        name: "Подтема № 1"
        grade: 3
    }
    ListElement {
        type: "subTopicTestRunnable"
        name: "Тест 1"
    }
    ListElement {
        type: "subTopicTest"
        name: "Тест 2"
        grade: 5
    }
}