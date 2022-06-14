import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts
import com.integrals.api

ApplicationWindow {
    id: appWindow
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
        anchors.centerIn: parent
        objectName: "pageLoader"
        id: pageLoader
        /* getFrame вызывает код из C++, выдавая нам в C++ необходимые объекты
        для взаимодействия с loader из кода */
        sourceComponent: LoaderManager.getFrame(appWindow)
    }
}
