import QtQuick 2.0

ListModel {
    ListElement {
        type: 'topic'
        topic_id: -1000
        name: 'TEST'
    }
    ListElement {
        type: 'topicTest'
        test_id: 1
        name: 'Тестовый тест'
        grade: 5
        attempts: 10
    }
}