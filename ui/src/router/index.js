import { createRouter, createWebHistory } from "vue-router";
import { getCookie } from "./../util/cookie-util.js";

const routes = [
  {
    path: "",
    name: "homepage",
    component: () => import("../components/HomePage.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/threatres",
    name: "threatres",
    component: () => import("../components/TheatreListPage.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/shows",
    name: "shows",
    component: () => import("../components/ShowListPage.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user-shows",
    name: "user-shows",
    component: () => import("../components/UserShowListPage.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/create-theatre",
    name: "create-theatre",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/CreateTheatre.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/create-show",
    name: "create-show",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/CreateShow.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/edit-show",
    name: "edit-show",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/EditShow.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/edit-theatre",
    name: "edit-theatre",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/EditTheatre.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/bookings",
    name: "bookings",
    component: () => import("../components/BookingListPage.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/book-show",
    name: "book-show",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/BookShow.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/show-bookings",
    name: "show-bookings",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/ShowBookingListPage.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "login",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/LogInForm.vue"),
    meta: {
      redirectHomeIfAlreadyLoggedIn: true,
    },
  },
  {
    path: "/register",
    name: "register",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../components/RegisterForm.vue"),
    meta: {
      redirectHomeIfAlreadyLoggedIn: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthTokenCookiePresent = !!getCookie("authToken");
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!isAuthTokenCookiePresent) {
      next({ name: "login" });
    } else {
      next(); // go to wherever I'm going
    }
  } else {
    if (
      to.matched.some((record) => record.meta.redirectHomeIfAlreadyLoggedIn) &&
      isAuthTokenCookiePresent
    ) {
      // If logged in, redirect to home page
      // Else, stay on the page
      if (localStorage.isAdmin == "1") {
        next({ name: "threatres" });
      } else {
        next({ name: "shows" });
      }
    } else {
      next(); // does not require auth, make sure to always call next()!
    }
  }
});

export default router;
