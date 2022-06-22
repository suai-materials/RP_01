import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15

Item{
ColumnLayout {
        anchors.centerIn: parent
        Image{
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 179
            Layout.preferredHeight: 179
            source: "qrc:/drawable/wifi_off.png"
        }
        Text {
                Layout.preferredWidth: 400
                Layout.preferredHeight: 100
                text: "К сожалению, доступ к нашим серверам недоступен"
                font.capitalization: Font.MixedCase
                font.family: "Roboto"
                font.pixelSize: 36
                color: "#ffffff"
                wrapMode: Text.Wrap
                font.weight: Font.Medium
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
        }
        RoundButton{
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 335
            Layout.preferredHeight: 60
            Layout.topMargin: 20
            contentItem: Text {
                text: "Повторить подключение"
                font.capitalization: Font.MixedCase
                font.family: "Roboto"
                font.pixelSize: 24
                color: "#9499B7"
                font.weight: Font.Medium
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onClicked: {
                loaderManager.reload()
            }
            Material.background: "#F8FDFF"
            radius: 24
        }
        RoundButton{
            Layout.alignment: Qt.AlignHCenter
            id: offlineBtn
            Layout.preferredWidth: 280
            Layout.preferredHeight: 55
            contentItem: Text {
                text: "Изучить темы офлайн"
                font.capitalization: Font.MixedCase
                font.family: "Roboto"
                font.pixelSize: 20
                color: "#9499B7"
                font.weight: Font.Medium
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onClicked: {
                loaderManager.mode = "Offline"
                loaderManager.frame_now = "topics.qml"
            }
            Material.background: "#FFF7FF"
            radius: 24
        }
}
}
