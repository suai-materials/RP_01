import QtQuick 2.0

ListModel {
    ListElement {
        type: 'topic'
        topic_id: -1000
        name: 'Введение'
        grade: 4
    }
    ListElement {
        type: 'topicTest'
        test_id: 1
        name: 'Тестовый тест'
        grade: 0
        attempts: 1999
    }
    ListElement {
        type: 'topic'
        topic_id: 1
        name: 'Неопределённый интеграл'
        grade: 2
    }
    ListElement {
        type: 'topicTest'
        test_id: 2
        name: 'Промежуточная проверка знаний'
        grade: 0
        attempts: 0
    }
}