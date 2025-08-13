/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class MaintenanceSound extends Component {
    setup() {
        this.env.bus.addEventListener('activity_assigned', this._onActivityAssigned.bind(this));
    }

    _onActivityAssigned(event) {
        const data = event.detail;
        if (data.user_id === this.env.session.uid && 
            (data.res_model === 'machinery.machine' || data.res_model === 'machinery.maintenance')) {
            this._playNotificationSound();
        }
    }

    _playNotificationSound() {
        // Only play sound after user interaction to avoid browser blocking
        if (document.hasFocus()) {
            const audio = new Audio('/machinery_maintenance/static/src/audio/notification.mp3');
            audio.volume = 0.3;
            audio.play().catch(() => {
                // Fallback: Use Web Notifications if audio fails
                if ('Notification' in window && Notification.permission === 'granted') {
                    new Notification('Maintenance Assignment', {
                        body: 'You have been assigned a new maintenance task',
                        icon: '/machinery_maintenance/static/description/icon.png'
                    });
                }
            });
        }
    }
}

registry.category("main_components").add("MaintenanceSound", {
    Component: MaintenanceSound,
});