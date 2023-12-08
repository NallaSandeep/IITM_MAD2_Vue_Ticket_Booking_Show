<template>
  <section class="vh-100">
    <div class="container-fluid h-custom">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-9 col-lg-6 col-xl-5">
          <section class="jumbotron text-center">
            <div class="container">
              <h1 class="jumbotron-heading">Edit Theatre Details</h1>
              <h2 class="jumbotron-heading">Theatre Admin Panel</h2>
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
            @submit="editTheatre"
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
              <label class="form-label" for="theatre-name">Theatre name</label>
              <input
                type="text"
                id="theatre-name"
                class="form-control form-control-lg"
                name="theatre-name"
                v-model="theatrename"
                required
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="area">Place</label>
              <input
                type="text"
                id="area"
                class="form-control form-control-lg"
                name="area"
                v-model="area"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label" for="city">City</label>
              <input
                type="text"
                class="form-control form-control-lg"
                id="city"
                name="city"
                v-model="city"
                required
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="capacity">Capacity</label>
              <input
                type="number"
                class="form-control form-control-lg"
                id="capacity"
                name="capacity"
                v-model="capacity"
                required
              />
            </div>
            <div class="mb-3 d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg btn-block">
                Update Theatre Details
                <span
                  v-if="showLoading"
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                >
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "EditTheatre",
  data() {
    return {
      errors: [],
      theatrename: null,
      area: null,
      city: null,
      capacity: null,
      showLoading: false,
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async editTheatre(e) {
      this.showLoading = true;
      e.preventDefault();
      this.errors = [];
      if (!this.theatrename) {
        this.errors.push("Theatre name required");
      }
      if (!this.area) {
        this.errors.push("Area required");
      }
      if (!this.city) {
        this.errors.push("City required");
      }
      if (!this.capacity) {
        this.errors.push("Capacity required");
      }
      if (!this.errors.length) {
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const userid = localStorage.userid;
        const theatreId = localStorage.theatreId;
        const authTokenCookieValue = getCookie("authToken");
        headers.append("Authentication-Token", authTokenCookieValue);
        const request = new Request(
          "http://localhost:5000/api/" + userid + "/theatre/" + theatreId,
          {
            method: "PUT",
            body: JSON.stringify({
              name: this.theatrename,
              area: this.area,
              city: this.city,
              capacity: this.capacity,
            }),
            headers: headers,
          }
        );
        await fetch(request)
          .then((response) => {
            if (response.status !== 200) {
              return response.json().then((errorData) => {
                // Extract error message from the response body
                const errorMessage =
                  errorData.message || "Unable to edit theatre";
                throw new Error(errorMessage);
              });
            }
            return response.json();
          })
          .then(() => {
            this.$router.push({ name: "threatres" });
          })
          .catch((error) => {
            this.errors.push(error.message);
          });
        this.showLoading = false;
      }
      this.showLoading = false;
    },
    async fetchData() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const userid = localStorage.userid;
      const theatreId = localStorage.theatreId;
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" + userid + "/theatre/" + theatreId,
        {
          method: "GET",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to fetch theatre";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.theatrename = data.name;
          this.area = data.area;
          this.city = data.city;
          this.capacity = data.capacity;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
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
