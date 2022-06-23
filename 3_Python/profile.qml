import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.0

Item{
    Rectangle {
        height: parent.height
        width: 264
        ColumnLayout{
            anchors.top: parent.top
            Image {
                id: img
                Layout.margins: 20
                source: 'https://sun9-10.userapi.com/impf/wRfqoB0IOyPhLSlCMRK9D5QRnYS83ASyhPiHsg/dBqabqWzCsw.jpg?size=658x603&quality=96&sign=7f27119c420587e05dcd142cf58a383a&type=album'
                Layout.preferredWidth: 224
                Layout.preferredHeight: 224
                fillMode: Image.PreserveAspectCrop
                layer.enabled: true
                layer.effect: OpacityMask {
                    maskSource: mask
                }
            }

            Rectangle {
                id: mask
                width: 224
                height: 224
                radius: 250
                visible: false
            }

            Text{
                id: first_name
                text: loaderManager.get
                color: "#000000"
                font.family: "Roboto"
                font.pixelSize: 20
            }
            Text{
                id: last_name
                text: "Фамилия"
                color: "#000000"
                font.family: "Roboto"
                font.pixelSize: 20
            }

        }
    }
    Rectangle {
        height: parent.height
        anchors.right: parent.right
        width: parent.width - 264
        color: "#FFF7FF"
        ColumnLayout{
            anchors.top: parent.top
            anchors.topMargin: 20
            Text{
            }
        }
    }
}