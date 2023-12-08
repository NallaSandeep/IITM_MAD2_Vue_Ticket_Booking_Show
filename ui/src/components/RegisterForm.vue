<template>
  <section class="vh-100">
    <div class="container-fluid h-custom">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-9 col-lg-6 col-xl-5">
          <section class="jumbotron text-center">
            <div class="container">
              <h1 class="jumbotron-heading">Registration</h1>
              <h2 class="jumbotron-heading">Unlock Your Theatre Experience</h2>
              <img
                src="../assets/images/login_page.webp"
                class="img-fluid"
                alt="Sample image"
              />
            </div>
          </section>
        </div>

        <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
          <form
            method="POST"
            id="register_user_form"
            @submit="register"
            novalidate="true"
          >
            <div class="mb-3">
              <div v-if="errors.length" class="text-danger">
                <b>Please correct the following error(s):</b>
                <ul>
                  <li
                    v-for="error in errors"
                    v-bind:key="error"
                    class="text-danger"
                  >
                    {{ error }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label" for="username">Full name</label>
              <input
                type="text"
                id="username"
                class="form-control form-control-lg"
                name="username"
                v-model="username"
                required
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="email">Email address</label>
              <input
                type="text"
                id="email"
                class="form-control form-control-lg"
                name="email"
                v-model="email"
                required
              />
            </div>

            <!-- Password input -->
            <div class="mb-3">
              <label class="form-label" for="password">Password</label>
              <input
                type="password"
                class="form-control form-control-lg"
                id="password"
                name="password"
                v-model="password"
                required
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="isAdmin">Type</label>
              <select
                class="form-select form-select-lg"
                id="isAdmin"
                v-model="isAdmin"
              >
                <option value="0" selected>Retail</option>
                <option value="1">Business</option>
              </select>
            </div>
            <div class="mb-3 d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg btn-block">
                Register
                <span
                  v-if="showLoading"
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                >
                </span>
              </button>
            </div>

            <div class="text-center">
              <p>Already a member? <a href="/login">Login</a></p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { getCookie, setCookie } from "./../util/cookie-util.js";
import { mapState, mapMutations } from "vuex";
export default {
  name: "LogInForm",
  data() {
    return {
      errors: [],
      username: null,
      email: null,
      password: null,
      isAdmin: 0,
      showLoading: false,
    };
  },
  computed: {
    ...mapState(["isLoggedIn"]),
  },
  methods: {
    ...mapMutations(["setIsLoggedIn"]),
    async register(e) {
      this.showLoading = true;
      e.preventDefault();
      this.errors = [];
      if (!this.username) {
        this.errors.push("Full name required");
      }
      if (!this.email) {
        this.errors.push("Email required");
      } else {
        if (!this.validEmail(this.email)) {
          this.errors.push("Invalid Email");
        }
      }
      if (!this.password) {
        this.errors.push("Password required");
      } else {
        if (!this.validPassword(this.password)) {
          this.errors.push("Password must be at least 8 characters");
        }
      }
      if (!this.errors.length) {
        const formData = new FormData();
        formData.append("username", this.username);
        formData.append("email", this.email);
        formData.append("password", this.password);
        formData.append("isAdmin", this.isAdmin);
        const request = new Request("http://localhost:5000/signup", {
          method: "POST",
          body: formData,
        });
        const response = await fetch(request)
          .then((response) => {
            if (response.status !== 201) {
              return response.json().then((errorData) => {
                // Extract error message from the response body
                const errorMessage =
                  errorData.message || "Unable to create account";
                throw new Error(errorMessage);
              });
            }
            return response.json();
          })
          .catch((error) => {
            this.errors.push(error.message);
          });
        this.showLoading = false;
        setCookie("authToken", response.token, 25);
        const authTokenCookieValue = getCookie("authToken");
        this.setIsLoggedIn(!!authTokenCookieValue);
        localStorage.isAdmin = response.isAdmin;
        localStorage.username = response.username;
        localStorage.email = response.email;
        localStorage.userid = response.id;
        if (response.isAdmin == "1") {
          this.$router.push({ name: "threatres" });
        } else {
          this.$router.push({ name: "shows" });
        }
      }
      this.showLoading = false;
    },
    validEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    validPassword: function (password) {
      return password.length >= 8;
    },
  },
};
</script>

<style scoped>
.h-custom {
  height: calc(100% - 73px);
}
@media (max-width: 450px) {
  .h-custom {
    height: 100%;
  }
}
</style>
