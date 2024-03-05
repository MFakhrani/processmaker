import Index from './components/Index.vue';
import Edit from './components/Edit.vue';
import InboxRuleSavedSearch from './components/InboxRuleSavedSearch.vue';

Vue.use(VueRouter);
const router = new VueRouter({
    mode: "history",
    base: "/tasks/rules",

    // See https://v3.router.vuejs.org/guide/
    routes: [
        {
            name: "index",
            path: "/",
            component: Index,
        },
        {
            name: "saved-search",
            path: "/saved-search",
            component: InboxRuleSavedSearch,
            props(route) {
                return {
                    savedSearchId: parseInt(route.query.saved_search_id),
                    processId: parseInt(route.query.process_id),
                    elementId: route.query.element_id,
                };
            }
        },
        {
            name: "edit",
            path: "/:id",
            component: Edit,
        },
    ],
});

new Vue({
    router,
}).$mount("#inbox-rules");