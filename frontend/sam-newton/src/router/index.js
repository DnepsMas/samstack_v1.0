import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NewtonView from '../views/NewtonView.vue'
import NewtonMoments from '../views/NewtonMoments.vue' // 引入新文件
import TestView from '../views/TestView.vue'
import PomodoroPage from '../views/PomodoroPage.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/newton',
            name: 'chat',
            component: NewtonView
        },
        {
            path: '/newton/moments',
            name: 'moments',
            component: NewtonMoments
        },
        {
            path: '/newton/test',
            name: 'test',
            component: TestView
        },
        {
            path: '/pomodoro',
            name: 'Pomodoro',
            component: PomodoroPage,
        }
    ]
})

export default router