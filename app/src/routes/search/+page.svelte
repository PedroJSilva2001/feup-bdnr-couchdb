<script>
	import { goto } from '$app/navigation';
	let firstName = '';
	let lastName = '';
	let condition = '';
	let patients = [];
	let serverLoaded = false;
	let search = false;

	async function handleSearch() {
		search = true;
		if (firstName && lastName) {
			const url = `http://localhost:8888/keyword-search/patient-by-name?first=${firstName}&last=${lastName}`;
			const response = await fetch(url);
			const data = await response.json();
			patients = data.results;
			serverLoaded = true;
		} else {
			alert('Please enter both a first and last name.');
		}
	}

	async function handleConditionSearch() {
		search = true;
		if (condition) {
			const url = `http://localhost:8888/keyword-search/patient-by-condition?condition=${condition}`;
			const response = await fetch(url);
			const data = await response.json();
			patients = data.results;
			serverLoaded = true;
		} else {
			alert('Please enter a condition.');
		}
	}
</script>

<button
	class="route-button profile-button"
	on:click={() => {
		goto('/profile');
	}}>My Profile</button
>
<button
	class="route-button logout-button"
	on:click={() => {
		localStorage.removeItem('ssn');
		localStorage.removeItem('pid');
		goto('/');
	}}>Logout</button
>
<div class="container">
	<h1>Search Patients</h1>
	<div class="search-forms">
		<div class="search-form">
			<label for="first-name">First Name:</label>
			<input id="first-name" type="text" bind:value={firstName} placeholder="First Name" />
			<label for="last-name">Last Name:</label>
			<input id="last-name" type="text" bind:value={lastName} placeholder="Last Name" />
			<button on:click={handleSearch}>Search</button>
		</div>
		<div class="search-form">
			<label for="condition">Condition:</label>
			<input id="condition" type="text" bind:value={condition} placeholder="Condition" />
			<button on:click={handleConditionSearch}>Search</button>
		</div>
	</div>
	<div class="search-results">
		<h3>Results</h3>
		{#if !serverLoaded && search}
			<div class="loading"><h3><i class="fa fa-spinner fa-spin" /> Loading</h3></div>
		{:else if Object.keys(patients).length > 0 && serverLoaded}
			{#each patients as patient}
				<div class="card">
					<p><strong>Name:</strong> {patient.prefix} {patient.first} {patient.last}</p>
					<p><strong>Birthdate:</strong> {patient.birthdate}</p>
					<p><strong>SSN:</strong> {patient.ssn}</p>
					<p><strong>Gender:</strong> {patient.gender}</p>
				</div>
			{/each}
		{:else}
			<div class="card">
				<p>No patients found.</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.search-forms {
		display: flex;
		flex-direction: row;
		justify-content: center;
	}

	.search-form {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 1rem;
		margin-right: 1rem;
	}

	.search-form input {
		margin-bottom: 0.5rem;
	}

	.search-results {
		width: 100%;
	}
	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	.fa-spinner {
		font-size: 2rem;
	}
	h3 {
		font-size: 2rem;
	}
	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.route-button {
		position: absolute;
		top: 20px;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 10%;
		color: white;
		padding: 1rem 2rem;
		text-align: center;
		font-size: 1rem;
		cursor: pointer;
	}

	.profile-button {
		right: 10rem;
	}
	.logout-button {
		right: 1rem;
	}
</style>
