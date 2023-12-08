<template>
  <main role="main">
    <section class="jumbotron text-center">
      <div class="container">
        <h2 class="jumbotron-heading">Theatre Management</h2>
        <p class="lead text-muted">
          Effortlessly manage and elevate your theatre venue with our all-in-one
          admin platform. Streamline operations, optimize revenue, and create
          unforgettable experiences.
        </p>
        <p>
          <a href="/create-theatre" class="btn btn-primary my-2"
            >Enroll a Theatre</a
          >
        </p>
      </div>
    </section>

    <div class="album py-4 bg-light">
      <div class="container">
        <div class="row">
          <div class="col-md-6 mb-3">
            <input
              type="text"
              class="form-control"
              placeholder="Search..."
              v-model="query"
            />
          </div>
          <div class="col-md-6" v-if="pageCount > 1">
            <pagination
              :currentPage="currentPage"
              :pageCount="pageCount"
              @page-changed="handlePageChange"
            />
          </div>
        </div>
        <div class="row" v-if="totalTheatreCount === 0">
          <p>No Theatre available</p>
        </div>
        <div class="row" v-else>
          <theatre-card
            v-for="(theatre, index) in filteredTheatres"
            :key="index"
            :userId="theatre.userId"
            :theatreId="theatre.theatreId"
            :name="theatre.name"
            :area="theatre.area"
            :city="theatre.city"
            :capacity="theatre.capacity"
            @reloadTheatreList="reloadTheatreList"
          />
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import TheatreCard from "./TheatreCard";
import PaginationComponent from "./PaginationComponent";
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "TheatreListPage",
  data() {
    return {
      theatres: [],
      errors: [],
      showLoading: false,
      totalTheatreCount: 0,
      pageCount: 0,
      currentPage: 1,
      query: "",
    };
  },
  components: {
    "theatre-card": TheatreCard,
    pagination: PaginationComponent,
  },
  mounted() {
    this.fetchTheatreList();
    this.fetchTheatreCount();
  },
  computed: {
    filteredTheatres() {
      return this.theatres.filter(
        (theatre) =>
          theatre.name.toLowerCase().includes(this.query.toLowerCase()) ||
          theatre.area.toLowerCase().includes(this.query.toLowerCase()) ||
          theatre.city.toLowerCase().includes(this.query.toLowerCase())
      );
    },
  },
  methods: {
    async fetchTheatreList() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const userid = localStorage.userid;
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          userid +
          "/theatres?page=" +
          this.currentPage +
          "&size=8",
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
                errorData.message || "Unable to fetch theatres";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.theatres = data;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async fetchTheatreCount() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const userid = localStorage.userid;
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" + userid + "/theatres/pages?size=8",
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
                errorData.message || "Unable to fetch theatres page count";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.totalTheatreCount = data.itemCount;
          this.pageCount = data.pageCount;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.fetchTheatreList();
    },
    async reloadTheatreList() {
      this.fetchTheatreList();
      this.fetchTheatreCount();
    },
  },
};
</script>

<style>
:root {
  --jumbotron-padding-y: 1rem;
}

.jumbotron {
  padding-top: var(--jumbotron-padding-y);
  padding-bottom: var(--jumbotron-padding-y);
  margin-bottom: 0;
  background-color: #fff;
}

.jumbotron p:last-child {
  margin-bottom: 0;
}

.jumbotron-heading {
  font-weight: 300;
}

.jumbotron .container {
  max-width: 40rem;
}

.box-shadow {
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.05);
}
</style>
