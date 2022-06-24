import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQml 2.15
import "models"
// import "qrc:/items/"
Item{
    GridView {
        id: grid
        anchors.leftMargin: 20
        anchors.topMargin: 10
        anchors.fill: parent
        cellWidth: width / Math.floor(width / 200)
        cellHeight: cellWidth + grid.cellWidth * 0.1
        model: TopicModel{}
        ScrollBar.vertical: ScrollBar {
            visible: true
        }
        delegate:
        Rectangle{
            color: "#FFF7FF"
            id: rect
            width: grid.cellWidth - 20
            height: grid.cellHeight - 20
            radius: 18
            Column{
                anchors.fill: parent
                id: column
                Image {
                    width: parent.width * 0.7
                    height: parent.height * 0.7
                    fillMode: Image.PreserveAspectFit
                    source: Qt.resolvedUrl(topic_icon)
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.topMargin: parent.height * 0.15
                }
                Text {
                    height: parent.height * 0.3
                    width: rect.width
                    text: topic_id + " " + name
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: "#9499B7"
                    font.family: "Roboto"
                    font.weight: Font.Medium
                    font.pixelSize: grid.cellHeight * 0.085
                    wrapMode: Text.WordWrap
                }
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    loaderManager.open_webpage(pageLoader, url, name, "Topic")
               }
            }
        }
    }
}
