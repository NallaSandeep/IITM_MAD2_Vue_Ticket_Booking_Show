<template>
  <section class="vh-100">
    <div class="container-fluid h-custom">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-9 col-lg-6 col-xl-5">
          <section class="jumbotron text-center">
            <div class="container">
              <h1 class="jumbotron-heading">Update Show</h1>
              <h3 class="jumbotron-heading">
                Revamp Your Spectacular Presentation!
              </h3>
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
              <label class="form-label" for="show-name">Show name</label>
              <input
                type="text"
                id="show-name"
                class="form-control form-control-lg"
                name="show-name"
                v-model="showname"
                required
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="rating">Rating (out of 5)</label>
              <input
                type="number"
                id="rating"
                class="form-control form-control-lg"
                name="rating"
                v-model="rating"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label" for="startTime">Start time</label>
              <flat-pickr
                id="datetime"
                class="form-control form-control-lg"
                v-model="startTime"
                :config="dateTimeConfig"
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="endTime">End time</label>
              <flat-pickr
                id="datetime"
                class="form-control form-control-lg"
                v-model="endTime"
                :config="dateTimeConfig"
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="tags">Tags</label>
              <input
                type="text"
                class="form-control form-control-lg"
                id="tags"
                name="tags"
                data-role="tagsinput"
                v-model="tags"
                required
              />
            </div>
            <div class="input-group input-group-lg mb-3">
              <span class="input-group-text" id="price-text">Price</span>
              <span class="input-group-text" id="rupee-icon">₹</span>
              <input
                type="number"
                id="price"
                class="form-control form-control-lg"
                name="price"
                v-model="price"
                required
              />
            </div>
            <div class="mb-3 d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg btn-block">
                Update Show
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
import FlatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import moment from "moment";
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "EditShow",
  data() {
    return {
      errors: [],
      showname: null,
      rating: null,
      startTime: null,
      endTime: null,
      tags: null,
      price: null,
      showLoading: false,
      dateTimeConfig: {
        enableTime: true, // Enable time selection
        dateFormat: "Y-m-d h:i K", // Date and time format
        altInput: true, // Display a human-readable date
        altFormat: "F j, Y h:i K", // Human-readable date format
      },
    };
  },
  computed: {
    formattedStartTime() {
      return this.startTime == null
        ? null
        : moment(this.startTime, "YYYY-MM-DD h:mm A").format(
            "YYYY-MM-DD HH:mm"
          );
    },
    formattedEndTime() {
      return this.endTime == null
        ? null
        : moment(this.endTime, "YYYY-MM-DD h:mm A").format("YYYY-MM-DD HH:mm");
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async register(e) {
      this.showLoading = true;
      e.preventDefault();
      this.errors = [];
      if (!this.showname) {
        this.errors.push("Show name required");
      }
      if (!this.rating) {
        this.errors.push("Rating required");
      }
      if (!this.startTime) {
        this.errors.push("Start time required");
      }
      if (!this.endTime) {
        this.errors.push("End time required");
      }
      if (!this.tags) {
        this.errors.push("Tags required");
      }
      if (!this.price) {
        this.errors.push("Price required");
      }
      if (!this.errors.length) {
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const authTokenCookieValue = getCookie("authToken");
        headers.append("Authentication-Token", authTokenCookieValue);
        const request = new Request(
          "http://localhost:5000/api/" +
            localStorage.userid +
            "/theatre/" +
            localStorage.theatreId +
            "/show/" +
            localStorage.showId,
          {
            method: "PUT",
            body: JSON.stringify({
              name: this.showname,
              rating: this.rating,
              startTime: this.formattedStartTime,
              endTime: this.formattedEndTime,
              tags: this.tags,
              price: this.price,
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
                  errorData.message || "Unable to update show";
                throw new Error(errorMessage);
              });
            }
            return response.json();
          })
          .then(() => {
            this.$router.push({ name: "user-shows" });
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
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
          "/theatre/" +
          localStorage.theatreId +
          "/show/" +
          localStorage.showId,
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
          this.showname = data.name;
          this.rating = data.rating;
          this.startTime = data.startTime;
          this.endTime = data.endTime;
          this.tags = data.tags;
          this.price = data.price;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
  },
  components: {
    flatPickr: FlatPickr,
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
