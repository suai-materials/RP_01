import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQml 2.15
// import "qrc:/items/"
Item{
GridView {
    id: grid
    anchors.leftMargin: 20
    anchors.topMargin: 10
    anchors.fill: parent
    cellWidth: width / 4
    cellHeight: cellWidth + grid.cellWidth * 0.1
    model: TopicModel {}
    ScrollBar.vertical: ScrollBar {
        visible: true
    }
    delegate:
    Rectangle{
        color: "#FFF7FF"
        width: column.width
        height: column.height
        radius: 18
        Column{
            id: column
            Image {
                width: grid.cellWidth - 40
                height: grid.cellHeight - 40 - grid.cellHeight * 0.08
                fillMode: Image.PreserveAspectFit
                source: topic_icon
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Text {
                text: name
                anchors.horizontalCenter: parent.horizontalCenter
                color: "#9499B7"
                font.family: "Roboto"
                font.weight: Font.Medium
                font.pixelSize: grid.cellHeight * 0.08
            }
        }
    }
}
}
