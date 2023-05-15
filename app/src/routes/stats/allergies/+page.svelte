<script>
	import { goto } from '$app/navigation';
	let allergyCode = '';
	let state = '';
	let city = '';
	let incidence = [];
	let serverLoaded = false;
	let search = false;

	async function handleAllergySearch() {
		search = true;
		if (allergyCode) {
			let url = `http://localhost:8888/encounter-stats/allergy-incidence?startkey=[${allergyCode}`;
			if (state) {
				url += `, "${state}"`;
				if (city) {
					url += `, "${city}"`;
				}
			}
			url += ']&endkey=[' + allergyCode;
			if (state) {
				url += `, "${state}"`;
				if (city) {
					url += `, "${city}"`;
				}
			}
			url += ']';
			const response = await fetch(url);
			const data = await response.json();
			incidence = data.results;
			serverLoaded = true;
		} else {
			alert('Please enter an allergy code.');
		}
	}
</script>

<button
	class="route-button profile-button"
	on:click={() => {
		goto('/profile');
	}}
>
	My Profile
</button>
<button
	class="route-button logout-button"
	on:click={() => {
		localStorage.removeItem('ssn');
		localStorage.removeItem('pid');
		goto('/');
	}}
>
	Logout
</button>

<div class="container">
	<h1>Search Allergy Incidence</h1>
	<div class="search-forms">
		<div class="search-form">
			<label for="allergy-code">Allergy Code:</label>
			<input id="allergy-code" type="text" bind:value={allergyCode} placeholder="Allergy Code" />
			<label for="state">State:</label>
			<input id="state" type="text" bind:value={state} placeholder="State" />
			<label for="city">City:</label>
			<input id="city" type="text" bind:value={city} placeholder="City" />
			<button on:click={handleAllergySearch}>Search</button>
		</div>
	</div>
	<div class="search-results">
		<h3>Results</h3>
		{#if !serverLoaded && search}
			<div class="loading">
				<h3><i class="fa fa-spinner fa-spin" /> Loading</h3>
			</div>
		{:else if Object.keys(incidence).length > 0 && serverLoaded}
			{#each incidence as result}
				{#each result.value as value}
					<div class="card">
						<p><strong>Description:</strong> {value.description}</p>
						<p><strong>Category:</strong> {value.category}</p>
						<p><strong>Count:</strong> {value.count}</p>
					</div>
				{/each}
			{/each}
		{:else}
			<div class="card">
				<p>No results found.</p>
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
