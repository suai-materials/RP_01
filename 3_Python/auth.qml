import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15

Item{
ColumnLayout {
        anchors.centerIn: parent
        Image{
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 224
            Layout.preferredHeight: 213
            source: "qrc:/drawable/sticker.png"
        }
        Image {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 376
                Layout.preferredHeight: 64
                // fillMode: Image.PreserveAspectFit
                source: "qrc:/drawable/telegram_auth.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        Qt.openUrlExternally("http://integrals.pank.su/?session=" + loaderManager.session_id) // Добавить SessionID
                   }
                }
        }
        RoundButton{
            Layout.alignment: Qt.AlignHCenter
            id: offlineBtn
            Layout.preferredWidth: 274
            Layout.preferredHeight: 60
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
                loaderManager.frame = "topics.qml"
            }
            Material.background: "#FFF7FF"
            radius: 24
        }
}
}
