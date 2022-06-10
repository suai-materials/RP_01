import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts
import com.integrals.splashscreen 1.0


ApplicationWindow {
    minimumWidth: 700
    minimumHeight: 500
    width: 1000
    height: 633
    visible: true
    Material.theme: Material.System
    Material.primary: "#C5CAE9"
    Material.background: "#C5CAE9"
    title: qsTr("integrals.pank.su")
    Loader{
        id: pageLoader
    }
    SplashScreen{
    }
    ColumnLayout{
        anchors.centerIn: parent
        Rectangle{
            Layout.alignment: Qt.AlignHCenter
            width: 196
            height: 196
            radius: 24
            Material.background: "#ffffff"
            Image{
                anchors.fill: parent
                anchors.centerIn: parent
                anchors.margins: 10
                source: "qrc:/drawable/logo.png"
            }
        }
        Pane{
            Layout.alignment: Qt.AlignHCenter
            RowLayout{
                spacing: 0
                Label{
                    text: qsTr("integrals")
                    font.pointSize: 24
                    Material.foreground: "#ffffff"
                    // horizontalAlignment: Text.AlignRight
                }
                Label {
                    text: qsTr(".pank.su")
                    font.pointSize: 24
                    Material.foreground: "#80FFFFFF"
                    // horizontalAlignment: Text.AlignLeft
                }
            }
        }
    }


}
