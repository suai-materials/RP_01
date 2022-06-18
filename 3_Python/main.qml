import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import io.integrals.LoaderManager 1.0
import QtWebEngine 1.10


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
    LoaderManager{
        id: loaderManager
    }

    Loader{
        anchors.centerIn: parent
        objectName: "pageLoader"
        id: pageLoader
        source: loaderManager.frame_now
        /* getFrame вызывает код из C++, выдавая нам в C++ необходимые объекты
        для взаимодействия с loader из кода */
        // sourceComponent: LoaderManager.getFrame()
    }
    ColumnLayout {
        anchors.centerIn: parent
        visible: loaderManager.auth_visible
        Image{
            Layout.preferredWidth: 224
            Layout.preferredHeight: 213
            source: "./res/sticker.png"
        }
        property WebEngineView webView: webView_
        WebEngineView{
            id: webView_
            Layout.preferredWidth: 260
            Layout.preferredHeight: 60
            backgroundColor: "transparent"
            url: "http://integrals.pank.su"
//            onNewWindowRequested: function(request) {
//                var newWindow = parent.createObject(appWindow);
//                newWindow.webView.acceptAsNewWindow(request);
//            }
        }
    }
}
