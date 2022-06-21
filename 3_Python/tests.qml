import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtQml 2.15
import "models"

Item{
    ListView {
        id: listView
        spacing: 60
        contentHeight: 10
        anchors.margins: 10
        contentWidth: parent.width
        anchors.fill: parent
        model: TestsModel {}
        delegate:
        Item{
            Rectangle{
                height: row.height
                radius: 12
                color: "#FFF7FF"
                anchors.left: parent.left
                anchors.leftMargin: type === "topic" ? 0 : (type.includes("sub") ? (type === "subTopic" ? listView.contentWidth * 0.1 : listView.contentWidth * 0.2) : listView.contentWidth * 0.1)
                width: listView.contentWidth - anchors.leftMargin - 20
                Row {
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    height: 48
                    id: row
                    Image{
                        id: run_test
                        anchors.verticalCenter: parent.verticalCenter
                        width: 35
                        height: 35
                        source: type !== "topic" ? "qrc:/drawable/test_icon.png" : "qrc:/drawable/topics_icon.svg"
                    }
                    Text {
                        text: name
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: run_test.right
                        anchors.leftMargin: 10
                        color: "#9499B7"
                        font.family: "Roboto"
                        font.weight: Font.Medium
                        font.pixelSize: 20
                    }

                }

            }
        }
    }
}