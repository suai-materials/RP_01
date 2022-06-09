import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts


ApplicationWindow {
//    minimumWidth: 700
//    minimumHeight: 500
    width: 1000
    height: 633
    visible: true
    Material.theme: Material.System
    Material.primary: "#C5CAE9"
    Material.background: "#C5CAE9"
    title: qsTr("integrals.pank.su")
    Rectangle{
        width: 196
        height: 196
        anchors.centerIn: parent
        radius: 20
        Material.background: "#ffffff"
        Image{
            anchors.fill: parent
            anchors.centerIn: parent
            anchors.margins: 10
            source: "qrc:/drawable/logo.png"
        }
    }


//    GridLayout{
//        anchors.fill: parent

//    }
}
