<script>
	import { goto } from '$app/navigation';

	let ssn = '';
	async function handleLogin() {
		const res = await fetch(`http://localhost:8888/patient/${ssn}`);
		const data = await res.json();

		if (data) {
			localStorage.removeItem('pid');
			localStorage.removeItem('ssn');
			localStorage.setItem('ssn', ssn);
			// redirect to profile page
			goto('/profile');
		} else {
			alert('Invalid SSN');
		}
	}
</script>

<h1>Login</h1>
<div class="container">
	<label for="ssn">SSN</label>
	<input type="text" id="ssn" bind:value={ssn} />
	<button on:click={handleLogin}>Login</button>
</div>

<style>
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: auto;
		margin-bottom: auto;
	}
	label {
		font-size: 1.5rem;
	}
	input {
		padding: 5px;
		font-size: 16px;
		width: 50%;
	}
	button {
		padding: 10px;
		font-size: 16px;
		cursor: pointer;
		width: 25%;
		margin-top: 1.5rem;
	}
</style>
