import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import QtWebEngine 1.10

WebEngineView{
    id: webView
    url: Qt.resolvedUrl(pageLoader.url)
    backgroundColor: "transparent"
}


